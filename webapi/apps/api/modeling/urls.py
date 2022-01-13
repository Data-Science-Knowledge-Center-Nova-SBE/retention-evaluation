from django.urls import path
from . import controllers

urlpatterns = [
    # train
    path("train/", controllers.train),
    path("train/state/", controllers.train_state),

    # modleing
    path("predict/9-grade", controllers.predict_9_grade, name="prediction-9-grade"),
    path("predict/8-grade", controllers.predict_8_grade, name="prediction-8-grade"),
    path("predict/6-grade", controllers.predict_6_grade, name="prediction-6-grade"),
]
