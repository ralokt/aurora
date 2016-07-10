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


def merge_query_dict(query_dict_A, query_dict_B):

    assert isinstance(query_dict_B, QueryDict), "update argument has to be a QueryDict()"

    merged = QueryDict(mutable=True)
    merged.update(query_dict_A)

    for key in query_dict_B.keys():
        if key in merged:
            merged.setlist(key, list(set(query_dict_A.getlist(key) + query_dict_B.getlist(key))))
        else:
            merged.setlist(key, query_dict_B.getlist(key))

    return merged


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


def suspicion_filters_from_request(request, course, elaboration_id=None):

    filter_args = request.session.get('suspicion_filter_args', {})

    filter_args['suspect_doc__submission_time__year'] = 2016
    filter_args['similar_doc__submission_time__year'] = 2014

    state_filter = request.GET.get('state', None)
    if state_filter is not None:
        state_filter = int(state_filter)
        if state_filter >= 0:
            filter_args['state'] = state_filter
            request.session['suspicion_page_number'] = 1
        else:
            if 'state' in filter_args:
                del filter_args['state']

    request.session['suspicion_filter_args'] = filter_args

    if elaboration_id:
        filter_args['suspect_doc__elaboration_id'] = elaboration_id
        request.session['suspicion_page_number'] = 1
    else:
        if request.GET.get('page', None) is not None:
            request.session['suspicion_page_number'] = int(request.GET.get('page'))

    page = request.session.get('suspicion_page_number', 1)

    return (filter_args, page)


def render_plagcheck_suspicion_list(request, course, suspect_elaboration_id=None):

    queryset = Suspicion.objects.all()
    is_embedded_in_details = False
    if suspect_elaboration_id:
        is_embedded_in_details = True
        queryset.filter(suspect_doc__elaboration_id=suspect_elaboration_id)

    suspicion_query_filter = SuspicionQueryFilter(request.GET, queryset=queryset)

    session_filter = query_dict_from_session(request, 'suspicion_filter_querydict')
    if session_filter:
        suspicion_query_filter.data = merge_query_dict(suspicion_query_filter.data, session_filter)
        # check if filter has been changed
        if not is_query_dict_equal(session_filter, suspicion_query_filter.data, exclude=['page']):
            suspicion_query_filter.data['page'] = 1

    request.session['suspicion_filter_querydict'] = suspicion_query_filter.data.copy()

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
    (filter_args, page_number) = suspicion_filters_from_request(request, course)

    (prev_suspicion_id, next_suspicion_id) = suspicion.get_prev_next(**filter_args)

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
