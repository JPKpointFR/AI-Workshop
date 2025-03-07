# Assistant Poétique avec Reconnaissance Vocale et Synthèse Vocale

Ce projet combine la reconnaissance vocale, l'intelligence artificielle de Mistral pour générer des réponses poétiques, et la synthèse vocale via Eleven Labs pour fournir des réponses sous forme d'audio.

## Fonctionnalités
1. **Reconnaissance vocale** : Utilisation de la bibliothèque `speech_recognition` pour écouter les questions de l'utilisateur via un microphone.
2. **IA Poétique** : Les réponses sont générées par Mistral avec une personnalité poétique, dyslexique qui bégaye et utilise des figures de style surprenantes.
3. **Synthèse vocale** : Utilisation de la bibliothèque `ElevenLabs` pour transformer les réponses textuelles en audio.
4. **Lecture audio** : L'audio généré est joué via `pygame`.

## Prérequis

Avant de commencer, vous devez installer les bibliothèques nécessaires :

```bash
pip install elevenlabs SpeechRecognition pygame requests
