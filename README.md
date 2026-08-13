# DjangoChat 💬

A real-time chat application built with Django, HTMX, WebSockets, and a suspicious amount of Redis.

DjangoChat lets users join chat rooms, exchange messages in real time, and customize their profiles — all without repeatedly refreshing the page like it's 2009.

## ✨ Features

- 💬 **Real-time chat rooms**
  - Create and browse chat rooms.
  - Join a room and see its messages.
  - Messages appear instantly for everyone currently connected to the room.

- ⚡ **WebSocket-powered communication**
  - Bidirectional communication between the browser and server.
  - No page refresh required when another user sends a message.
  - Messages are broadcast to connected users in the same room.

- 🧩 **HTMX integration**
  - HTML is exchanged directly between the server and browser.
  - Minimal custom JavaScript.
  - WebSocket responses can update the page without a full reload.

- 👤 **User profiles**
  - User-specific profile information.
  - Profile pictures can be uploaded and updated.

- 🖼️ **Media storage**
  - Profile pictures and other media assets are stored using Amazon S3.

- 📱 **Responsive UI**
  - Styled with Tailwind CSS.
  - DaisyUI provides reusable UI components without turning every button into a small CSS research project.

- 🚀 **Production deployment**
  - Configured for deployment on Render.
  - PostgreSQL for production database storage.
  - Redis/Render Key Value for the WebSocket channel layer.
  - WhiteNoise for serving static assets.

---

## 🛠️ Technology Stack

### Backend

- **Python**
- **Django**
- **Django Channels**
- **PostgreSQL**
- **Redis**

Django handles the application itself, while Django Channels extends it with WebSocket support for real-time communication.

### Frontend

- **HTML**
- **HTMX**
- **HTMX WebSocket Extension**
- **Tailwind CSS**
- **DaisyUI**

The application follows an HTML-over-the-wire approach where Django remains responsible for generating much of the UI rather than pushing all application logic into a large JavaScript frontend.

### Storage

- **PostgreSQL** — application data
- **Amazon S3** — uploaded media and profile pictures
- **WhiteNoise** — static files

### Deployment

- **Render Web Service** — Django application
- **Render PostgreSQL** — production database
- **Render Key Value** — Redis-compatible backend for Django Channels

---

## 🏗️ How It Works

The interesting part of DjangoChat is the communication flow.

When a user opens a chat room, the browser establishes a WebSocket connection with the Django application:

```text
Browser
   │
   │ WebSocket connection
   ▼
Django Channels
   │
   ▼
Channel Layer
   │
   ▼
Redis
```

When the user sends a message, Django can save it to the database and broadcast it to the other users connected to the same room.

```text
                 Django
                /      \
               /        \
              ▼          ▼
        Browser A    Browser B
              │          │
              └── Chat ──┘
```

Browser B doesn't need to ask:

> "Hey Django, anything new?"

Django can simply say:

> "Yep. Here's a message."

And HTMX takes care of updating the appropriate part of the page.

---

## 📂 Core Architecture

At a high level, the application separates its responsibilities like this:

```text
                         ┌──────────────┐
                         │   Browser    │
                         │ HTMX + WS    │
                         └──────┬───────┘
                                │
                           WebSocket
                                │
                                ▼
                     ┌──────────────────┐
                     │      Django      │
                     │  Django Channels │
                     └────────┬─────────┘
                              │
                       Channel Layer
                              │
                              ▼
                           Redis
                              │
                     Broadcast messages
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
           Connected User              Connected User


Django ──────────────► PostgreSQL
        application data

Django ──────────────► Amazon S3
        media files

Django ──────────────► WhiteNoise
        static assets
```

---

## 🧠 Why WebSockets?

Traditional HTTP communication generally looks like:

```text
Browser → Request → Server
Browser ← Response ← Server
```

That's perfectly fine for many applications.

Chat is different.

If ten people are sitting in the same room, we don't want every browser constantly asking the server whether someone said something new.

WebSockets give us a persistent communication channel:

```text
Browser ⇄ Server
```

That allows the server to push new messages to connected clients immediately.

This makes WebSockets a natural fit for real-time features such as chat.

---

## 🔐 Authentication & User Context

Messages are associated with authenticated users, allowing the application to distinguish who sent each message and display the appropriate user information.

Each user can also have a profile picture, making the conversation slightly more human and slightly less like two database rows arguing with each other.

---

## 🚀 Running the Project

Clone the repository and create a virtual environment:

```bash
git clone <repository-url>
cd djangochat

python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
python manage.py migrate
python manage.py runserver
```

Make sure Redis is available when running the WebSocket functionality locally.

---

## 🌍 Production

The production architecture uses Render services for the main infrastructure:

```text
Render
│
├── Web Service
│   └── DjangoChat
│
├── PostgreSQL
│   └── Application database
│
└── Key Value
    └── WebSocket channel layer
```

Media files are stored separately in Amazon S3, while WhiteNoise handles static assets.

---

## 🎯 Project Goals

DjangoChat is designed around a simple idea:

> Keep the server responsible for the application and let the browser receive the HTML it needs — even when that HTML arrives through a WebSocket.

The result is a real-time application without requiring a heavyweight frontend framework to manage the entire UI.

Less JavaScript.

More Django.

And just enough WebSockets to make refreshing the page feel personally offensive.

---
