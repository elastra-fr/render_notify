# Render Notify Addon for Blender (EN)

The addon is currently in its early stages of development, and the version is set to 0.0.1. The author is Emmanuel LASTRA DE NATIAS. The addon is designed to work with Blender version 4.0.0 and above (to be confirmed).

This addon provides a simple notification system for Blender's render process. It allows users to receive notifications when a render is complete, making it easier to manage long rendering tasks without having to constantly check the progress.

## Security

Credentials are stored via the `keyring` library, which securely manages sensitive information. This ensures that your email and/or Discord credentials are not exposed in plain text.

## Messages customization

The addon allows users to customize the notification messages that are sent when a render is complete. This feature enables users to personalize their notifications according to their preferences, making the experience more enjoyable and tailored to their needs.

## Channels 

The addon supports multiple notification channels, including for now 
- email 
- Discord. 

Users can choose their preferred method of receiving notifications, allowing for greater flexibility and convenience in managing their rendering workflow.

### Email

Users can set up email notifications to receive alerts when their renders are complete. This is particularly useful for those who want to stay informed without having to check Blender constantly.

Do not use a personal email address for this purpose. Instead, create a dedicated email account for sending notifications to ensure better security and management of your credentials. If you can use an app specific password, it is recommended to enhance security further.

### Discord

Users can also opt to receive notifications via Discord, which is a popular communication platform for gamers and communities. This allows users to stay connected and receive updates in real-time without leaving their workflow. To set up Discord notifications, users will need to create a webhook in their Discord server and provide the webhook URL in the addon's settings. This way, they can receive notifications directly in their chosen Discord channel when a render is complete.

## Tests 

A test suite with `pytest` is provided in `tests/`. The tests can be run outside of Blender thanks to fakes for `bpy` and `keyring`.

Prerequisite: `pytest` and virtual environment (recommended).

Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
```


Activate the virtual environment (Linux/MacOS) :

```bash
source .venv/bin/activate
```

Deactivate the virtual environment:

```bash
deactivate
```

Execution examples:

```bash
# in the project's virtual environment (recommended)
./.venv/bin/python3 -m pytest -v

# or globally
python3 -m pytest -v
```

Install `pytest` in the venv:

```bash
./.venv/bin/python3 -m pip install pytest
```


# Render Notify Addon pour Blender (FR)

L'addon est actuellement en cours de développement, et la version est définie à 0.0.1. L'auteur est Emmanuel LASTRA DE NATIAS. L'addon est conçu pour fonctionner avec Blender version 4.0.0 et supérieure (à confirmer).

Cet addon offre un système de notification simple pour le processus de rendu de Blender. Il permet aux utilisateurs de recevoir des notifications lorsque le rendu est terminé, facilitant ainsi la gestion des tâches de rendu longues sans avoir à vérifier constamment la progression.

## Sécurité

Les identifiants sont stockés via la bibliothèque `keyring`, qui gère de manière sécurisée les informations sensibles. Cela garantit que vos identifiants de messagerie et/ou Discord ne sont pas exposés en texte clair.

## Personnalisation des messages

L'addon permet aux utilisateurs de personnaliser les messages de notification envoyés lorsque le rendu est terminé. Cette fonctionnalité permet aux utilisateurs d'adapter les notifications à leurs préférences, rendant l'expérience plus agréable et personnalisée.

## Canaux

L'addon prend en charge plusieurs canaux de notification, y compris pour l'instant le courrier électronique et Discord. Les utilisateurs peuvent choisir leur méthode préférée pour recevoir les notifications, offrant ainsi une plus grande flexibilité et commodité dans la gestion de leur flux de travail de rendu.

### Courrier électronique

Les utilisateurs peuvent configurer des notifications par courrier électronique pour recevoir des alertes lorsque leurs rendus sont terminés. Cela est particulièrement utile pour ceux qui souhaitent rester informés sans avoir à vérifier constamment Blender.

Il est recommandé de ne pas utiliser une adresse e-mail personnelle à cet effet. Créez plutôt un compte e-mail dédié pour l'envoi des notifications afin d'assurer une meilleure sécurité et gestion de vos identifiants. Si vous pouvez utiliser un mot de passe spécifique à l'application, il est recommandé de renforcer encore la sécurité.

### Discord

Les utilisateurs peuvent également choisir de recevoir des notifications via Discord, qui est une plateforme de communication populaire pour les joueurs et les communautés. Cela permet aux utilisateurs de rester connectés et de recevoir des mises à jour en temps réel sans quitter leur flux de travail. Pour configurer les notifications Discord, les utilisateurs devront créer un webhook dans leur serveur Discord et fournir l'URL du webhook dans les paramètres de l'addon. Ainsi, ils pourront recevoir des notifications directement dans le canal Discord de leur choix lorsque le rendu est terminé.

## Tests

Une suite de tests basée sur `pytest` est fournie dans le répertoire `tests/`. Les tests sont conçus pour s'exécuter hors de Blender : un fake minimal pour `bpy` et `keyring` est utilisé afin d'éviter d'avoir besoin d'une installation de Blender pour lancer la suite.

Prérequis : `pytest` et environnement virtuel (recommandé).

Créer un environnement virtuel (optionnel mais recommandé) :

```bash
    python3 -m venv .venv
```
Activer l'environnement virtuel (Linux/MacOS) :

```bash
    source .venv/bin/activate
```

Désactiver l'environnement virtuel :

```bash
    deactivate
```

Exemples d'exécution :

```bash
# dans l'environnement virtuel du projet (recommandé)
./.venv/bin/python3 -m pytest -v

# ou avec l'interpréteur système
python3 -m pytest -v
```

To install `pytest` in the venv:

```bash
./.venv/bin/python3 -m pip install pytest
```

