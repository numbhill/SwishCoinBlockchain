# 🚀 SwishCoin Blockchain

SwishCoin is a **Django-based blockchain project** featuring a **decentralized Q&A platform, SwishCoin transactions, mining system, and blockchain explorer**. This project allows users to **earn, trade, and mine SwishCoins** while participating in a **Stack Overflow-style developer community**.

---

## **📌 Features**
- **💰 Digital Currency System:** Users receive SwishCoins upon signup and can send transactions.
- **⛏️ Mining System:** Users can mine transactions to earn SwishCoins.
- **🗃️ Blockchain Explorer:** View blocks, transactions, and user balances.
- **📊 Q&A Developer Community:** Users post questions and offer SwishCoin bounties for answers.
- **🏆 Best Answer Rewards:** The best answer to a question receives a SwishCoin bounty.
- **🛠️ Admin Panel:** Manage users, balances, and transactions.
- **🔐 Secure Authentication:** User registration and login using Django authentication.
- **🌐 Responsive UI:** Built with TailwindCSS for modern design.

---

# **🛠️ Tech Stack**
- **Backend:** Django (Python)
- **Database:** MySQL (phpMyAdmin)
- **Frontend:** TailwindCSS
- **Blockchain:** Custom-built using Django models
- **Version Control:** GitHub

---

# **🚀 Project Setup (Local Environment)**
Follow these steps to **set up and run SwishCoin locally**.

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-github-username/swishcoin-blockchain.git
cd swishcoin-blockchain
```
### **2️⃣ Set Up Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```
### **4️⃣ Configure MySQL Database**
- Open phpMyAdmin and create a new database:
- Database Name: swishcoin_db
- Update DATABASES settings in swishcoin/settings.py:
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swishcoin_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
### **5️⃣ Apply Migrations**
```sh
python manage.py makemigrations
python manage.py migrate
```
### **6️⃣ Create a Superuser**
```sh
python manage.py createsuperuser
```
### **7️⃣ Run the Development Server**
```sh
python manage.py runserver
```
