# FocusFlow

**An adaptive productivity and wellbeing app for students with ADHD**

FocusFlow is a Django web application built to support university students with ADHD in managing tasks, energy and daily structure.

The idea started from my own experience in the past 2 years at university. I was diagnosed with ADHD, and I received help with managing time and my condition from the University’s Wellbeing Hub.

One of the problems I wanted to address is that someone with ADHD might not have the same level of energy and focus every day.

## Main Features

### Daily Reset
The user selects their current energy level and mood. Based on their answers, FocusFlow gives them a suitable mode, an AI-generated suggestion and recommends routines and coping strategies that might be useful for that day.

### Task Management
Users can create, edit, complete and delete their tasks. Tasks can be marked as urgent and/or important using the Eisenhower Matrix idea.

### AI Task Generator
The user can describe a larger task or goal in their own words, and the Groq API breaks it down into smaller and more manageable tasks.

### Strategy Library
The Strategy Library contains practical coping techniques that students with ADHD can use when they need additional support.

### Routines
FocusFlow includes step-by-step routines for different activities, including Morning, Study, Evening, Cleaning and Cooking routines.

### Brain Dump
Brain Dump is a private space where users can quickly write down thoughts, worries, reminders or anything else they want to get out of their mind.

### Dopamine Menu
The Dopamine Menu provides a selection of small activities that the user can choose when they need a short break or mental reset.

### Personalisation
FocusFlow has nine selectable colour themes, including seasonal and dark themes. Each theme has its own matching background image so users can choose a design they find comfortable and attractive.

## Technologies Used

- **Backend:** Django 6.0
- **Python:** Python 3.14.3 locally / Python 3.12 on PythonAnywhere
- **Database:** SQLite and Django ORM
- **REST API:** Django REST Framework
- **Authentication:** Django authentication, Google SSO and JWT
- **Frontend:** Django templates, HTML, CSS and JavaScript
- **AJAX:** `fetch()` for live search and interactive features
- **AI:** Groq API
- **Deployment:** PythonAnywhere EU
- **Version Control:** GitHub

## Deployment

FocusFlow is deployed on PythonAnywhere and can be accessed online at:

https://mariafocusflow.eu.pythonanywhere.com/

## Future Development

There are still some features and improvements that I would like to add to FocusFlow in the future:

- Embedded videos in the Strategy Library
- Improved routine recommendations
- Time-zone support
