# 🚗 IFRI_comotorage

Application web de covoiturage pour les étudiants de l’IFRI, conçue dans le cadre du projet intégrateur 2024-2025.

---

## 📌 Objectif du projet

- Faciliter la mise en relation entre conducteurs et passagers au sein de la communauté universitaire pour partager des trajets de manière pratique, économique et sécurisée.
- Permettre aux étudiants de publier ou rechercher des trajets.
- Offrir un système de messagerie interne.
- Proposer un matching intelligent entre offres et demandes.
- Apporter une solution économique et écologique aux déplacements étudiants.

---

## 🛠️ Fonctionnalités principales

- ✅ Création de compte conducteur ou passager
- 🔍 Recherche intelligente de trajets disponibles
- 📅 Planification et réservation de trajets
- 💬 Messagerie instantanée entre utilisateurs
- 🔐 Authentification sécurisée
- 🧭 Interface responsive et intuitive

---

## 🧪 Technologies utilisées

- **Backend** : Python (Django) 
- **Frontend** : HTML5, CSS3, Bootstrap 5, JavaScript
- **Base de données** : MySQL ; MySQL Workbench
- **Outils** : Git & GitHub, VS Code

---

## 🧑‍💻 Membres du groupe

| Nom | Rôle |
|-----|------|
| TOVIGNAN Félix | Chef de projet, Développeur Backend |
| KPOGBEME Brunel | Testeur du projet, Développeur Backend |
| FAKEYE Grâce | Développeuse Frontend |
| VLAVONOU Best | UX/UI Designer |
| BAMIGBOLA Ulrich | Développeur Frontend |
| DADEOU Serge | Développeur Frontend |

---

## 📦 Installation & Déploiement

### Prérequis pour le déploiement

- Python 3.13+
- pip (installé avec Python)
- Git
- MySQL et MySQL Workbench

---

## :book: Étapes d'installation

1. **Cloner le dépôt :**

    ```bash
    git clone https://github.com/lenurb-123/PIL1_2425_26.git
    cd PIL1_2425_26
    ```

2. **Créer un environnement virtuel et l'activer :**

    ```bash
    python -m venv venv
    # Pour Linux/MacOS
    source venv/bin/activate
    # Pour Windows
    venv\Scripts\activate
    ```

3. **Installer les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

---

___

## Configuration de la base de données 

### Option 1 : Utiliser le fichier structure.sql (méthode démo)

1. **Créer une base de données MySQL appelée `ifri_comotorage`**

2. **Importer le fichier dans l'invite de commandes shell de MySQL avec la commande **

    ```bash
    mysql -u root -p ifri_comotorage < db/structure.sql
    ```

3. **Modifier le fichier `settings.py`  de votre application principale IFRI_comotorage:**

    ```python
    DATABASES = {
         'default': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'ifri_comotorage',
              'USER': 'root',
              'PASSWORD': 'votre_mot_de_passe',
              'HOST': 'localhost',
              'PORT': '3306',
         }
    }
    ```

4. **Données de connexion**
   
     - Compte superutilistateur
        - Email : admin@gmail.com
        -  Mot de passe : admin123 

     - Compte 1 : Compte passager 
        - Email : kpogbemebrunel@gmail.com
        - Mot de passe : 12345678

    - Compte 2 : Compte Conducteur 
        - Email : felix@gmail.com
        - Mot de passe : 111213
    

    - Compte 3 : Compte Passager
        - Email : ulrich@gmail.com
        - Mot de passe : 101112

---

### Option 2 : Créer la base manuellement avec MySQL Workbench 

- **Créer la base de données MySQL appelée `ifri_comotorage`**

- **Modifier le fichier `settings.py`  de votre application  principale IFRI_comotorage :**

    ```python
    DATABASES = {
         'default': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'ifri_comotorage',
              'USER': 'root',
              'PASSWORD': 'votre_mot_de_passe',
              'HOST': 'localhost',
              'PORT': '3306',
         }
    }
    ```

---


## :arrow_down: Accéder au dossier IFRI_comotorage

```bash
    cd IFRI_comotorage
```

## :arrow_forward: Démarrer le projet:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## :airplane: Lancer le projet 

```bash
python manage.py runserver
```


Ouvrir le navigateur : [https://127.0.0.1:8000](https://127.0.0.1:8000)




---

# :+1: Pour tester la messagerie , veillez ouvrir le lien dans différents navigateurs avec différents comptes pour vous envoyer des messages 

---

# :aerial_tramway:Contribuer 

**Les contributions sont les bienvenues**

1. Fork le projet

2. Crée une branche (git checkout -b feature/Nom)

3. Commit tes modifications (git commit -m 'Ajout fonctionnalité')

4. Push (git push origin feature/Nom)

5. Ouvre une Pull Request

# :classical_building: Nos Coordonnateurs 

## Equipe pedagogique

- Supervision: **M. Ratheil HOUNDJI**
  ---
- Encadrants:
    - **M.Armand ACCROMBESSI** 
    - **Mme .Maryse GAHOU**
  
---

# 💯 Pour plus d'informations sur les téléchargements des paquets et d'instructions très détaillés , veillez consultez le rapport.html 


