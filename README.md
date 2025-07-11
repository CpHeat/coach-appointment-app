# Coach App

> Plateforme de prise de rendez-vous entre clients et coaches, avec gestion des rôles et annotations des séances.

---

## ✨ Fonctionnalités principales

* ✅ Prise de rendez-vous en ligne
* 📅 Historique des rendez-vous (passés & à venir)
* ✏️ Annotation des rendez-vous par les coaches
* 🔄 Annulation de rendez-vous
* 👤 Gestion des profils
* 📊 Dashboard indiquant :

  * Rendez-vous à venir
  * Rendez-vous passés
  * Nombre total de clients & de rendez-vous
* 🔐 Authentification multi-rôles :

  * **Admin** : création de comptes coaches, accès total à l’administration
  * **Coach** : accès à ses propres rendez-vous & annotations
  * **Client** : accès à ses propres rendez-vous uniquement

---

## 🖥️ Stack technique

* **Backend** : Django
* **Base de données** : SQLite
* **Frontend** : Tailwind CSS intégré via [`django-tailwind`](https://django-tailwind.readthedocs.io/)
* Rendu **100% server-side**, pas d’API publique.

---

## 📂 Structure du projet

```
coach_appointment_project/
│
├── coach_appointment_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── coach_appointment_site/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   ├── coach_appointment_site/
│   │   ├── emails/
│   │   └── registration/
│   ├── templatetags/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── registration.py
│   │   └── site.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── tokens.py
│   └── urls.py
│
├── node_modules/
│
├── theme/          # django-tailwind theme
│   ├── static/
│   └── static_src/
│       └── src/
│           └── css/
│
└── manage.py
```

---

## 🚀 Installation & lancement local

1. **Cloner le projet :**

   ```bash
   git clone <repo-url>
   cd coach_appointment_project
   ```

2. **Créer un environnement virtuel :**

   ```bash
   python -m venv venv
   source venv/bin/activate  # sous Linux/macOS
   venv\Scripts\activate     # sous Windows
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   npm install --prefix theme
   ```

6. **Lancer le serveur de développement :**

   ```bash
   python manage.py tailwind start
   python manage.py runserver
   ```

---

## ⚠️ Remarques importantes

* Les **avatars utilisés dans l’application sont générés et ne correspondent pas à de vraies personnes.**
* La base de données par défaut est SQLite, prévue pour un usage local ou en développement.

---

## 📝 Licence

Ce projet est sous licence MIT.
Voir le fichier [`LICENSE`](LICENSE) pour plus d’informations.

---
