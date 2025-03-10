from elevenlabs import ElevenLabs
import speech_recognition as sr
import requests
import pygame
import time
import os

ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
PERSONNALITE = "ROLE------------------ à définir"

historique = []

client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)

def generer_reponse_mistral(prompt):
	headers = {
		"Authorization": f"Bearer {MISTRAL_API_KEY}",
		"Content-Type": "application/json"
	}
	data = {
		"model": "mistral-large-latest",
		"messages": [
			{"role": "system", "content": PERSONNALITE},
			{"role": "user", "content": prompt}
		],
		"max_tokens": 80,
		"temperature": 0.5
	}
	response = requests.post(MISTRAL_CHAT_URL, headers=headers, json=data)
	if response.status_code == 200:
		return response.json()["choices"][0]["message"]["content"].strip()
	else:
		raise Exception(f"Erreur API Mistral : {response.status_code} - {response.text}")

def main():
	recognizer = sr.Recognizer()

	pygame.mixer.init()

	print("Salut. Je suis prêt à discuter avec toi.")
	while True:
		try:
			with sr.Microphone() as source:
				print("Parle-moi (dis 'stop' pour arrêter) :")
				recognizer.adjust_for_ambient_noise(source, duration=1)
				audio = recognizer.listen(source)
		except Exception as e:
			print(f"Erreur avec le microphone : {e}")
			continue
		try:
			question = recognizer.recognize_google(audio, language="fr-FR")
			print(f"Tu as dit : {question}")
			if question.lower() == "stop":
				print("À bientôt.")
				break
		except sr.UnknownValueError:
			continue
			print(question)
		except Exception as e:
			print(f"Erreur de reconnaissance vocale : {e}")
			continue
		historique.append(f"Utilisateur : {question}")
		prompt = "\n".join(historique)
		try:
			reponse = generer_reponse_mistral(prompt)
		except Exception as e:
			print(f"Erreur lors de la génération : {e}")
			continue
		historique.append(f"Assistant : {reponse}")
		print(f"Assistant : {reponse}")
		fichier_audio = "reponse.mp3"
		try:
			audio_stream = client.generate(
				text=reponse,
				voice="Rachel",
				model="eleven_multilingual_v2",
				voice_settings={"stability": 0.9, "similarity_boost": 0.5}
			)
			with open(fichier_audio, "wb") as f:
				for chunk in audio_stream:
					f.write(chunk)
		except Exception as e:
			print(f"Erreur lors de la synthèse vocale avec ElevenLabs : {e}")
			continue
		try:
			pygame.mixer.music.load(fichier_audio)
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy():
				time.sleep(0.1)
		except Exception as e:
			print(f"Erreur lors de la lecture audio : {e}")
		finally:
			if os.path.exists(fichier_audio):
				os.remove(fichier_audio)

if __name__ == "__main__":
	main()
