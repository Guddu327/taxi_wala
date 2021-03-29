from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from background_task import background
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView

from rides.utils.API.google_api_util.API import GoogleApiHandler
from ..decorators import rider_required
from ..forms import RiderSignUpForm, BookRideViewForm
from ..models import Status, User, Ride, Executive, Place

class RiderSignUp(CreateView):
    model = User
    form_class = RiderSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'rider'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('rider:book')

@method_decorator([login_required, rider_required], name='dispatch')
class SetLocation(CreateView):
    model = Ride
    form_class = BookRideViewForm
    template_name = 'rides/rider/get_ride.html'
    # success_url = reverse_lazy('rider:live')

    gAPI = GoogleApiHandler()
    



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_oq = Status.objects.get(name="On Queue").ride_set.all()
        status_og = Status.objects.get(name="Ongoing").ride_set.all()
        onqueue_ride = status_oq.filter(rider=self.request.user).first()
        ongoing_ride = status_og.filter(rider=self.request.user).first()
        print(onqueue_ride)
        print(ongoing_ride)
        if not onqueue_ride and not ongoing_ride:
            context["ride_flag"] = 0
            context["r_pk"] = 1
        elif not ongoing_ride:
            context["ride_flag"] = 1
            context["r_pk"] = onqueue_ride.pk
        else:
            context["ride_flag"] = 2
            context["r_pk"] = ongoing_ride.pk

        print(context["ride_flag"])
        print(context["r_pk"])
        return context
    
    def form_valid(self, form):
        # messages.success(self.request, 'Interests updated with success!')
        ride = form.save(commit=False)
        ride_status = Status.objects.get(name="On Queue")
        ride.status = ride_status
        ride.rider = self.request.user
        ride.save()
        return redirect('rider:live', ride.pk)

@method_decorator([login_required, rider_required], name='dispatch')
class BookRide(DetailView):
    model = Ride
    template_name = 'rides/rider/check_ride.html'

    gAPI = GoogleApiHandler()

    @background(schedule=40)
    def create_car_posititons(self, source):
        # lookup user by id and send them a message
        coor = self.gAPI.get_coor(source)
        random_loc = self.gAPI.random_points(2.0, coor)
        curr_cab = Cab.objects.get()
        cab = Cab
        ride.save()
            print (ride.)
        return 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride = self.get_object()
        data = self.gAPI.calculate_distance(orig=ride.source, dest=ride.destination)
        ride.travelled = int(data['rows'][0]['elements'][0]['distance']['value'])/1000
        total_duration = data['rows'][0]['elements'][0]['duration']['value']
        ride.charges = self.gAPI.calculate_cost(ride.travelled, total_duration)
        ride.save()
        get_coor = 
        create_car_posititons(ride.source, ride)
        # first_cab = 
        context['rider'] = ride.rider
        context['cab'] = ride.cab
        context['cabee'] = ride.cabee
        return context

@method_decorator([login_required, rider_required], name='dispatch')
class RideView(DetailView):
    model = Ride
    context_object_name = 'ride'
    template_name = 'rides/rider/ride_status.html'

    def get_context_data(self, **kwargs):
        kwargs['rider'] = self.get_object().rider
        
        kwargs['cabee'] = self.get_object().cabee

        return super().get_context_data(**kwargs)

@method_decorator([login_required, rider_required], name='dispatch')
class PastRides(ListView):
    model = Ride
    
    def get_queryset(self, **kwargs):
        rider = self.request.user.rider
        queryset = Ride.objects.filter(rider=rider)
        return queryset

# @login_required
# @rider_required
# def update_ride(request, pk):
    
