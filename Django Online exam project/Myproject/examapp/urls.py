from django.urls import path
from . import views

urlpatterns = [
   
   path("next/",views.nextpage),
   path("back/",views.previousQuestion),
   path("endexam/",views.endexam),
   path('starTest/',views.starTest),
   path('view_resultdata/',views.view_resultdata),
   path('search_user/',views.search_user),
   path('addquestions/',views.addquestions),
   path("updatequestions/",views.updatequestions),
   path("viewquestions/",views.viewquestions),
   path('deletequestions/',views.deletequestion),
   path('managequestiondata/',views.managequestiondata),
   path('backtodashboard/',views.backtodashboard),
   # path("search_page/<pageno>/",views.search_page)
  

]
