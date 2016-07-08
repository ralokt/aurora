from django.template import RequestContext
from django.template.loader import render_to_string

from PlagCheck.models import Suspicion, SuspicionState


def suspicion_filters_from_request(request, course, elaboration_id=None):

    filter_args = request.session.get('suspicion_filter_args', {})

    filter_args['suspect_doc__submission_time__year'] = 2016

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


def render_plagcheck_suspicion_list(request, course, elaboration_id=None):
    (filter_args, page_number) = suspicion_filters_from_request(request, course, elaboration_id)

    open_new_window = False
    enable_state_filter = True
    if elaboration_id:
        open_new_window = True
        enable_state_filter = False

    print(filter_args)

    suspicion_list = Suspicion.objects.filter(**filter_args)

    count = suspicion_list.count()

    context = {
        'course': course,
        'suspicions': suspicion_list,
        'suspicion_states': SuspicionState.choices(),
        'current_suspicion_state_filter': int(filter_args.get('state', -1)),
        'suspicions_count': count,
        'open_new_window': open_new_window,
        'enable_state_filter': enable_state_filter,
        'page_number': page_number,
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
