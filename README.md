# 🚀 SwishCoin Blockchain Project Roadmap

This document outlines the **step-by-step roadmap** for the SwishCoin Blockchain Project, from **blockchain fundamentals** to **full feature implementation**.

---

## 📌 **Phase 1: Understanding Blockchain & Smart Contracts**
✔ Learn blockchain fundamentals: Blocks, Hashing, Consensus  
✔ Explore **Proof of Work (PoW)** & **Proof of Stake (PoS)**  
✔ Study **Bitcoin, Ethereum**, and real-world blockchain applications  
✔ Understand **Smart Contracts** and **Tokenomics**  
✔ Define **SwishCoin Supply Cap (1,000,000 SwishCoins max)**  

---

## 🛠 **Phase 2: Setting Up the Development Environment**
✔ Create the **Django project** (`SwishCoinBlockchain`)  
✔ Initialize a **virtual environment (venv)**  
✔ Install **Django, Django REST Framework**, and required libraries  
✔ Configure **MySQL and phpMyAdmin** as the database  
✔ Set up a **GitHub repository** for version control  

---

## ⛓️ **Phase 3: Implementing the Core Blockchain**
✔ Implement **Block & Blockchain classes** (Hashing, Transactions, Proof of Work)  
✔ Create API endpoints:  
   - `/api/get_chain` → Fetch full blockchain  
   - `/api/mine_block` → Mine a new block  
   - `/api/add_transaction` → Add transactions  
✔ Integrate `mine_transactions()` logic to add blocks  
✔ Implement **basic transaction validation** before adding to blockchain  

---

## 💰 **Phase 4: Implementing SwishCoin as a Limited Digital Currency**
### 🏛 **Step 1: Implement Supply Control & Admin Role**
✔ Define **`MAX_SUPPLY` (1,000,000 SwishCoins)**  
✔ Assign `SWISHCOIN_CREATOR` role (Super Admin)  
✔ Restrict **new SwishCoin creation beyond the max supply**  

### 👛 **Step 2: Implement User Wallets & Transaction System**
✔ Create **User Registration & Login System**  
✔ Users receive **100 SwishCoins upon signup** (if supply allows)  
✔ Implement SwishCoin **wallet balances in `UserProfile` model**  
✔ Create **Admin Panel (admin.py) for managing balances**  
✔ Implement **`register_user()` logic** to enforce supply limits  
✔ Users can **send SwishCoins to each other** (`add_transaction()` API)  

---

## 🙋‍♂️ **Phase 5: Implementing Developer Community (Q&A System)**
### ❓ **Step 1: Users Can Post Coding Questions**
✔ Create **Question model (`models.py`)**  
✔ Users can **post questions** with a SwishCoin bounty  
✔ Bounty amount is **deducted from user’s balance**  
✔ Implement **`post_question()` function**  
✔ Add API endpoint & test posting questions  

### 💡 **Step 2: Users Can Answer & Vote**
✔ Create **Answer model (`models.py`)**  
✔ Users can **submit answers** to coding questions  
✔ Users can **upvote/downvote** answers  
✔ Implement **`vote_answer()` function**  
✔ Add API endpoint & test voting system  

### 🏆 **Step 3: Reward the Best Answer**
✔ Implement **`reward_best_answer()` function**  
✔ The **answer with the most votes gets SwishCoin bounty**  
✔ SwishCoins **transfer from question owner to best answer provider**  
✔ Add API endpoint & test bounty transfer  

---

## 🎨 **Phase 6: Building the Q&A System UI**
### **Step 1: Implement Views (`views.py`)**
✔ **`ask_question()`** → Renders the question posting page  
✔ **`answer_question()`** → Renders the answer submission page  
✔ **`view_question()`** → Displays a single question with answers  
✔ **`vote_answer()`** → Allows users to vote on answers  
✔ **`select_best_answer()`** → Transfers bounty to the best answer  

### **Step 2: Implement UI Templates (`TailwindCSS`)**
✔ `ask_question.html` → Users post new coding questions  
✔ `view_question.html` → Displays question and answers  
✔ `answer_question.html` → Allows users to submit answers  

### **Step 3: Configure URLs (`urls.py`)**
✔ `/ask_question/` → Route for posting new questions  
✔ `/view_question/<int:question_id>/` → View question & answers  
✔ `/answer_question/<int:question_id>/` → Submit an answer  
✔ `/vote_answer/<int:answer_id>/` → Vote on an answer  
✔ `/select_best_answer/<int:answer_id>/` → Reward best answer  

---

## 🔍 **Phase 7: Designing the SwishCoin Explorer UI**
✔ Build a **Blockchain Explorer UI using TailwindCSS**  
✔ Create `index.html` with a **user-friendly layout**  
✔ Connect UI to the API using **JavaScript (Fetch API)**  
✔ Implement:
   - **`transactions.html`** → Shows all transactions  
   - **`balance.html`** → Displays user balance  
   - **`user_transactions.html`** → Displays transaction history  
✔ Implement **a responsive navigation bar (`navbar.html`)**  

---

## 🏁 **Phase 8: Final Testing Before Deployment**
### ✅ **User Authentication & Wallet System**
✔ Test **New User Registration** (Check Balance Distribution)  
✔ Test **Coin Supply Limits** (Ensure No Over-Issuance)  
✔ Verify **Admin Controls Over SwishCoin Balances**  

### 🛠 **Blockchain & Transactions**
✔ Test **Mining System** (Ensure rewards are credited correctly)  
✔ Test **Blockchain Validation** (No duplicate transactions)  
✔ Test **API Responses for Edge Cases**

---

## 🔮 **Future Enhancements**
🔹 **Implement Smart Contracts** for automated transactions  
🔹 **Introduce Staking Mechanism** for passive SwishCoin earnings  
🔹 **Real-time Notifications for transactions and mining**  
🔹 **Deploy as a Decentralized Application (DApp)**  
🔹 **Mobile App for iOS/Android** to manage SwishCoin Wallet  


