from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .models import Stat, User,Quiz,Scenario
from rest_framework.response import Response
from django.db import connection
from rest_framework import generics
from rest_framework import status
from .serializers import ScenarioSerializer
from rest_framework.parsers import MultiPartParser, FileUploadParser
# Create your views here.
from rest_framework.generics import RetrieveAPIView
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
class QuizView(APIView):
    def post(self,request):
        user_name=request.data['nom']
        user_email=request.data['email']
        user_score=0
        user=User.objects.create(name=user_name,email=user_email,score=user_score)
        user.save()
        nb_question=Scenario.objects.count()
        quiz=Quiz.objects.create(id_user=user,nbre_questions=nb_question,nbCorrect=0,nbFausse=0)
        quiz.save()
        return Response({
            "quiz_id":quiz.id
        })


class ScenarioView(APIView):
    def get(self, request):
        # Obtenir tous les scénarios
        quiz_id = request.query_params.get('quiz_id')
        scenarios = Scenario.objects.all().order_by('id')  # Trier par ID ou autre champ
        if not scenarios.exists():
            return Response({"error": "Aucun scénario disponible"}, status=404)

        # Retourner le premier scénario
        scenario = scenarios.first()
       
        quiz=Quiz.objects.get(id=quiz_id)
        user_id=quiz.id_user.id
        user=User.objects.get(id=user_id)
        data = {
            "id": scenario.id,
            "type": scenario.type,
            "titre": scenario.titre,
            "description": scenario.description,
            "image": scenario.image.url if scenario.image else None,
            "sender": scenario.sender,
            "sender_mail":scenario.sender_mail,
            "footer":scenario.footer,
            "button":scenario.button,
            "reponse":scenario.reponse,
            "explication":scenario.explication,
            "url":scenario.url,
            "objet":scenario.objet,
            "mail_body":scenario.mail_body,
            "user_name":user.name,
            "user_email":user.email,

        }
        return Response(data, status=200)

    def post(self, request):
        # Prendre l'ID du scénario actuel et la réponse de l'utilisateur
        scenario_id = request.data.get('scenario_id')
        quiz_id=request.data.get('quiz_id')
        user_answer = request.data.get('user_answer')  # True ou False

        try:
            scenario = Scenario.objects.get(id=scenario_id)
        except Scenario.DoesNotExist:
            return Response({"error": "Scénario non trouvé"}, status=404)

        # Vérifier la réponse de l'utilisateur
        is_correct = scenario.reponse == user_answer
        if is_correct:
            message = "Bravo! Vous avez donné la bonne réponse."
            quiz=Quiz.objects.get(id=quiz_id)
            quiz.nbCorrect+=1
            quiz.save()
        else:
            message = "Désolé! Votre réponse est incorrecte."
            quiz=Quiz.objects.get(id=quiz_id)
            quiz.nbFausse+=1
            quiz.save()
        return Response(
            {
                'message': message,
            }) 

class nextScenarioView(APIView):      # Obtenir le prochain scénario
    def post(self,request):
        scenario_id = request.data['scenario_id' ] # Récupérer l'id dans le corps de la requête
        quiz_id = request.data['quiz_id' ]
        next_scenario = Scenario.objects.filter(id__gt=scenario_id).order_by('id').first()
        quiz=Quiz.objects.get(id=quiz_id)
        user=User.objects.get(id=quiz.id_user.id)


        

        if next_scenario:
         next_data = {
            "id": next_scenario.id,
            "type": next_scenario.type,
            "titre": next_scenario.titre,
            "description": next_scenario.description,
            "image": next_scenario.image.url if next_scenario.image else None,
            "sender": next_scenario.sender,
            "sender_mail":next_scenario.sender_mail,
            "footer":next_scenario.footer,
            "button":next_scenario.button,
            "reponse":next_scenario.reponse,
            "explication":next_scenario.explication,
            "url":next_scenario.url,
            "objet":next_scenario.objet,
            "mail_body":next_scenario.mail_body,
            "user_name":user.name,
            "user_email":user.email
            }
        else:
            next_data = None

        return Response({
            
            "scenario": next_data,
        }, status=200)

class ResultView(APIView):
    def post(self,request):
        quiz_id=request.data['quiz_id']
        quiz=Quiz.objects.get(id=quiz_id)
        score=quiz.nbCorrect
        user=User.objects.get(id=quiz.id_user.id)
        user.score=score
        pourcentage = (quiz.nbCorrect / quiz.nbre_questions) * 100 if quiz.nbre_questions > 0 else 0
        stat = Stat.objects.create(
            id_user=user,
            nbre_questions=quiz.nbre_questions,
            nbCorrect=quiz.nbCorrect,
            nbFausse=quiz.nbFausse,
            score=quiz.nbCorrect,
            pourcentage=pourcentage
        )
        stat.save()
        if score>=quiz.nbre_questions/2:
            message="Bravo! Vous avez réussi le quiz "
        else:
            message="Désolé! Vous n'avez pas réussi le quiz "
        
       
        return Response({
            "score":score,
            "user_name":user.name,
            "message":message,
            "nbre_questions":quiz.nbre_questions,
            

        })
class ScenarioCreateView(generics.CreateAPIView):
    queryset = Scenario.objects.all()  # Indique que la vue interagira avec le modèle Scenario
    serializer_class = ScenarioSerializer  # Le sérialiseur à utiliser pour valider et serializer les données
    parser_classes = (MultiPartParser, FileUploadParser)


class ScenarioListView(APIView):
    def get(self, request):
        scenarios = Scenario.objects.all()
        serializer = ScenarioSerializer(scenarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ScenarioDeleteView(APIView):
    def delete(self, request, pk):
        scenario = get_object_or_404(Scenario, pk=pk)
        scenario.delete()
        return Response({"message": "Scénario supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    
class UpdateScenarioView(APIView):
    def put(self, request, pk):
        try:
            scenario = Scenario.objects.get(pk=pk)
        except Scenario.DoesNotExist:
            return Response({"error": "Scenario not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScenarioSerializer(scenario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScenarioDetailView(RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class StatistiquesAdminAPIView(APIView):
    def get(self, request):
        total_tests = Stat.objects.count()
        total_scenarios = Scenario.objects.count()
        moyenne_correctes = Stat.objects.aggregate(Avg('nbCorrect'))['nbCorrect__avg'] or 0
        stats = Stat.objects.aggregate(
            total_correct=Sum('nbCorrect'),
            total_questions=Sum('nbre_questions')
        )
        taux_reussite = (stats['total_correct'] / stats['total_questions'] * 100) if stats['total_questions'] else 0
        repartition = {
            "phishing": Scenario.objects.filter(reponse=True).count(),
            "non_phishing": Scenario.objects.filter(reponse=False).count()
        }

        tests_par_mois = (
            Stat.objects.annotate(month=TruncMonth('date_test'))
            .values('month')
            .annotate(total_tests=Count('id'))
            .order_by('month')
        )

        taux_reussite_par_mois = (
            Stat.objects.annotate(month=TruncMonth('date_test'))
            .values('month')
            .annotate(taux_reussite=Avg('pourcentage'))
            .order_by('month')
        )
        labels = []
        tests_data = []
        taux_data = []

        for entry in tests_par_mois:
            labels.append(entry['month'].strftime('%b %Y'))  # Format: "Jan 2024"
            tests_data.append(entry['total_tests'])

        for entry in taux_reussite_par_mois:
            taux_data.append(entry['taux_reussite'])
        data = {
            "total_tests": total_tests,
            "total_scenarios": total_scenarios,
            "moyenne_correctes": moyenne_correctes,
            "taux_reussite": taux_reussite,
            "repartition": repartition,
            "labels": labels,  # Mois (X-axis)
            "tests_data": tests_data,  # Nombre de tests par mois (Bar Chart)
            "taux_data": taux_data  #
        }
        return Response(data)
    

