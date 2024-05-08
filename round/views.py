from django.shortcuts import render, redirect
from .models import Course, HoleDetail, Score, Tip
from django.http import HttpResponse
from .forms import CourseForm, TipsForm, ScoreForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import datetime
import json, sys


def marker_pass(hole_num):
    loading_tips = {}
    tip_collected = []
    for x in Tip.objects.all().filter(hole_id=hole_num):
        loading_tips = {
            'type': 'Feature',
            'properties': {
                'description':
                    "<p>" + x.body + "<p>",
                'icon': x.icon
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [x.gps_cords_lat, x.gps_cords_long]
            }
        }
        tip_collected.append(loading_tips)
    
    return json.dumps(tip_collected,indent=4)

def home(request, course_id, holeNum, score_id):
    form = TipsForm()
    markers = marker_pass(holeNum)
    try:
        course = Course.objects.get(pk=course_id)
        hole = HoleDetail.objects.filter(course_id=course_id, hole_number=holeNum).first()
        allHoles = HoleDetail.objects.filter(course_id=course_id)
        totalYardage = sum(hole.yardage for hole in allHoles)
        tips = Tip.objects.filter(hole_id=hole.hole_id)
        score = Score.objects.get(pk=score_id)
        
        if request.method == "POST":
            form = TipsForm(request.POST)
            scoreForm = ScoreForm(request.POST)
            
            if scoreForm.is_valid():
                scoreValue = scoreForm.cleaned_data['score']
                setattr(score, f"hole_{holeNum}", scoreValue)
                score.save()
                #form.save()
                #scoreForm.save()
                return redirect('golf-home', course_id=course_id, holeNum=holeNum, score_id=score_id)
            
        else:
            scoreForm = ScoreForm(initial={'score': getattr(score, f'hole_{holeNum}', 0)})
        
        return render(request, 'round/tester.html', {'course': course, 'hole': hole, 'allHoles': allHoles, 'tips': tips, 'map_key': settings.MAPBOX_KEY, "markers": markers, "form": form, "score": score, "scoreForm": scoreForm, "totalYardage": totalYardage})

    except Course.DoesNotExist:
        messages.error(request, 'This course has not been set up yet, Please try again at a later time')
        return HttpResponseRedirect('/round/selection/')

def scorecard(request):
    return render(request, 'round/base.html')

def select_course(request):
    score = None
    states = Course.objects.values_list('state', flat=True).distinct()
    state_courses = {}

    for state in states:
        state_courses[state] = Course.objects.filter(state=state)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            selected_course_id = form.cleaned_data['course']
            score = Score.objects.create(
                player = request.user,
                course_id = Course.objects.get(course_id = selected_course_id),
                datetime_played = datetime.now()
            )
            score.save()
            return redirect('golf-home', course_id = selected_course_id, holeNum = 1, score_id = score.pk)
        else:
            messages.add_message(request, messages.INFO, "Error Please Select a course")
            form = CourseForm()
    else:
        form = CourseForm()
    return render(request, 'round/course_list.html', {'form': form, 'score': score, 'states': states, 'state_courses': state_courses})


def printScores(request):
    sort_option = request.GET.get('sort')
    user_scores = Score.objects.filter(player=request.user)

    # Need to add more sorting options...
    if sort_option == 'ascDate':
        user_scores = sorted(user_scores, key=lambda x: x.datetime_played)
    elif sort_option == 'descDate':
        user_scores = sorted(user_scores, key=lambda x: x.datetime_played, reverse=True)
    elif sort_option == 'ascScore':
        user_scores = sorted(user_scores, key=lambda x: x.round_total)
    elif sort_option == 'descScore':
        user_scores = sorted(user_scores, key=lambda x: x.round_total, reverse=True)

    score_details = []
    for score in user_scores:
        course = Course.objects.get(course_id=score.course_id.course_id)
        course_name = course.course_name
        course_city = course.city
        course_state = course.state
        hole_details = HoleDetail.objects.filter(course_id=score.course_id.course_id)
        total_yardage = sum(hole.yardage for hole in hole_details)
        total_par = sum(hole.par_number for hole in hole_details)
        score_details.append({
            'score': score,
            'hole_details': hole_details,
            'course_name': course_name,
            'course_state': course_state,
            'course_city': course_city,
            'total_yardage': total_yardage,
            'total_par': total_par
        })
    return render(request, 'round/score_list.html', {'score_details': score_details})


def delete_score(request, score_id):
    if request.method == 'POST':
        try:
            score = Score.objects.get(pk=score_id)
            score.delete()
        except Score.DoesNotExist:
            # do something for scorecard not existing
            pass
    # do something for invalid requests
    return redirect('golf-scorecard')
