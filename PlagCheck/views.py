from django.template import RequestContext
from django.template.loader import render_to_string
from django.http.request import QueryDict

from PlagCheck.models import Suspicion, SuspicionState, SuspicionQueryFilter


def query_dict_from_session(request, key):
    content = request.session.get(key, None)
    if content:
        ret = QueryDict(mutable=True)
        ret.update(content)
        return ret
    return None


def update_query_dict(target, update):

    assert isinstance(target, QueryDict), "target argument has to be a QueryDict()"
    target._assert_mutable()

    _update = update
    if not isinstance(_update, QueryDict):
        _update = QueryDict(mutable=True)
        _update.update(update)

    for key in update.keys():
        if key in target:
            target.setlist(key, list(set(target.getlist(key) + _update.getlist(key))))
        else:
            target.setlist(key, _update.getlist(key))


def is_query_dict_equal(dictA, dictB, exclude=[]):
    dictA_copy = dict(dictA.copy())
    dictB_copy = dict(dictB.copy())

    for key in exclude:
        try:
            del dictA_copy[key]
        except ValueError:
            pass

        try:
            del dictB_copy[key]
        except ValueError:
            pass

    return dictA_copy == dictB_copy


def suspicion_filters_from_request(request, extra_list_filters={}):

    suspicion_query_filter = SuspicionQueryFilter(request.GET, queryset=Suspicion.objects.all())

    # ensure filter data is a mutable QueryDict
    print("suspicion_query_filter.data: " + str(suspicion_query_filter.data))
    if not isinstance(suspicion_query_filter.data, QueryDict):
        print("create instance")
        suspicion_query_filter.data = QueryDict(mutable=True)
    else:
        suspicion_query_filter.data = suspicion_query_filter.data.copy()

    session_filter = query_dict_from_session(request, 'suspicion_filter_querydict')
    print("session_filter: " + str(session_filter))
    print("suspicion_query_filter.data: " + str(suspicion_query_filter.data.copy()))
    if session_filter:
        update_query_dict(suspicion_query_filter.data, session_filter)
        # check if filter has been changed
        if not is_query_dict_equal(session_filter, suspicion_query_filter.data, exclude=['page']):
            suspicion_query_filter.data['page'] = 1

    print(suspicion_query_filter.data)
    request.session['suspicion_filter_querydict'] = suspicion_query_filter.data.copy()

    update_query_dict(suspicion_query_filter.data, extra_list_filters)

    return suspicion_query_filter


def render_plagcheck_suspicion_list(request, course, extra_list_filters={}, is_embedded_in_details=False):

    suspicion_query_filter = suspicion_filters_from_request(request, extra_list_filters)

    count = suspicion_query_filter.count()

    context = {
        'course': course,
        'suspicions': suspicion_query_filter,
        'suspicions_count': count,
        'is_embedded_in_details': is_embedded_in_details,
        'page_number': suspicion_query_filter.data.get('page', 1),
    }

    request.session['selection'] = 'plagcheck_suspicions'
    request.session['count'] = count

    return render_to_string('plagcheck_suspicions.html', context, RequestContext(request))


def render_plagcheck_compare(request, course, suspicion_id):

    suspicion = Suspicion.objects.get(pk=suspicion_id)
    suspicion_query_filter = suspicion_filters_from_request(request)

    (prev_suspicion_id, next_suspicion_id) = suspicion.get_prev_next_by_queryset(suspicion_query_filter.qs)

    context = {
        'course': course,
        'suspicion': suspicion,
        'suspicion_states': SuspicionState.states(),
        'suspicion_states_class': SuspicionState.__members__,
        'next_suspicion_id': next_suspicion_id,
        'prev_suspicion_id': prev_suspicion_id,
        'similar_has_elaboration': suspicion.similar_doc.was_submitted_during(course),
        'suspect_has_elaboration': suspicion.suspect_doc.was_submitted_during(course)
    }

    return render_to_string('plagcheck_compare.html', context, RequestContext(request))
