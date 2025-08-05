# ⚙️ Percipio – Scalable Asynchronous Collaboration Backend

Percipio is a role-based collaboration backend system designed to streamline project-based work between providers and contributors. Built with Django, WebSockets, Redis, and Stripe, it handles everything from task lifecycle management and contributor applications to real-time communication and milestone-based payments.


## 🚩 Problem It Solves

Managing short-term contributors across projects is chaotic — there’s no structured task flow, no real-time updates, and no secure payout system. Percipio fixes this by providing a backend system that:

- Structures task states and permissions
- Enables real-time role-aware communication
- Tracks contributor applications and submissions
- Integrates payments via Stripe

---

## 🛠️ Features

- **Role-Based Access Control**: Providers & Contributors with separate capabilities
- **Project & Task Management**: Create projects, add tasks with deadlines and dynamic state transitions (`Open → In Progress → Submitted → Completed`)
- **Contributor Workflow**: Apply to tasks, track approval status via email, submit work if approved
- **Submission & Review**: Role-restricted submission views with version tracking
- **Real-Time Chat**: Private and group chat using Django Channels + Redis
- **Stripe Integration**: Milestone-based secure payouts with webhook-driven state updates
- **Notification System**: Email alerts for task approval/rejection and system events

---

## 🧱 Tech Stack

- **Backend**: Django, Django REST Framework  
- **Real-Time**: Django Channels, Redis (as Channel Layer)  
- **Database**: PostgreSQL  
- **Payments**: Stripe API  
- **Authentication**: Custom `AbstractUser` with role-based permissions  
- **Email**: Django email backend (SMTP or console for dev)

---

## 📐 System Architecture

```plaintext
[ Provider ]            [ Contributor ]
     |                        |
  Create Project          Apply to Task
     |                        |
 Create Task                Email Status
     |                        |
View Applications         Submit Work
     |                        |
 Review Submissions      Real-Time Chat
     |                        |
 Stripe Payment <-------> Webhook Update
````



---

## ⚙️ Setup Instructions

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/percipio.git
   cd percipio
   ```

2. **Create virtual environment & install dependencies**

   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure `.env` file**

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=your_postgres_url
   STRIPE_SECRET_KEY=your_stripe_key
   EMAIL_HOST_USER=your_email
   EMAIL_HOST_PASSWORD=your_password
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run Redis server (for Channels)**

   ```bash
   redis-server
   ```

6. **Start development server**

   ```bash
   python manage.py runserver
   ```

---

## 🧪 Testing

* Unit tests: `python manage.py test`
* Test Redis and WebSocket connections using Django Channels debug tools




