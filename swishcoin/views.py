import hashlib
import json
import time
from datetime import datetime
from hashlib import sha256
from decimal import Decimal
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import UserProfile, Question, Answer, Transaction, Block
from .blockchain import Blockchain
from .forms import SignUpForm, LoginForm

blockchain = Blockchain()


def home(request):
    return redirect('/explorer/')


def blockchain_explorer(request):
    chain = Block.objects.all().order_by("-timestamp")
    return render(request, "explorer.html", {"chain": chain})


def get_chain(request):
    chain_data = [block.__dict__ for block in blockchain.chain]
    return JsonResponse({"chain": chain_data, "length": len(blockchain.chain)}, safe=False)


@login_required
def mine_block(request):
    last_block = blockchain.get_last_block()
    previous_hash = last_block["hash"] if last_block else "0"

    # Fetch unprocessed transactions (previously mined=False)
    transactions = Transaction.objects.filter(transaction_type="transfer")[:5]

    if not transactions.exists():
        return render(request, "mine.html", {"message": "No transactions to mine"})

    # Process transactions and update their status to "mined"
    for tx in transactions:
        tx.transaction_type = "mining"
        tx.save()

    transaction_data = [
        {"sender": tx.sender.username if tx.sender else "System", "receiver": tx.receiver.username,
         "amount": float(tx.amount)}
        for tx in transactions
    ]

    # Create a new block in the blockchain
    new_block = blockchain.create_block(transactions=transaction_data, previous_hash=previous_hash)

    # Save mined block to the database
    Block.objects.create(
        previous_hash=new_block["previous_hash"],
        timestamp=new_block["timestamp"],
        nonce=new_block.get("nonce", 0),
        hash=new_block["hash"]
    )

    # ✅ Reward the miner with 10 SwishCoins
    miner_profile, created = UserProfile.objects.get_or_create(user=request.user)
    miner_reward = Decimal(10)
    miner_profile.balance += miner_reward
    miner_profile.save()

    # ✅ Create transaction for mining reward
    Transaction.objects.create(
        sender=None,  # Mining rewards have no sender
        receiver=request.user,
        amount=miner_reward,
        transaction_type="mining"
    )

    return render(request, "mine.html", {
        "message": f"Block {new_block['index']} mined successfully! You received {miner_reward} SwishCoins.",
        "block": new_block
    })


def calculate_hash(index, timestamp, transactions, previous_hash):
    """
    Generates a SHA-256 hash for a block.
    """
    block_string = f"{index}{timestamp}{transactions}{previous_hash}".encode()
    return sha256(block_string).hexdigest()


def proof_of_work(block_data):
    nonce = 0
    while True:
        text = f"{block_data}{nonce}".encode()
        hash_result = hashlib.sha256(text).hexdigest()
        if hash_result[:4] == "0000":  # Target difficulty (adjustable)
            return nonce, hash_result
        nonce += 1


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, balance=100.0)
        return JsonResponse({"message": "User registered successfully!"})


@login_required
def send_swishcoin(request):
    if request.method == "POST":
        receiver_username = request.POST.get("receiver")
        amount = Decimal(request.POST.get("amount"))  # Convert amount to Decimal

        sender_profile = UserProfile.objects.get(user=request.user)
        receiver = User.objects.filter(username=receiver_username).first()

        if not receiver:
            return render(request, "profile.html", {"profile": sender_profile, "error": "Recipient not found!"})

        receiver_profile = UserProfile.objects.get(user=receiver)

        if sender_profile.balance >= amount:
            sender_profile.balance -= amount  # Now both are Decimal
            receiver_profile.balance += amount
            sender_profile.save()
            receiver_profile.save()

            # Store transaction in DB
            Transaction.objects.create(sender=request.user, receiver=receiver, amount=amount)

            return redirect("transactions")  # Redirect to transaction history page
        else:
            return render(request, "profile.html", {"profile": sender_profile, "error": "Insufficient balance!"})

    return redirect("profile")


@login_required
def post_question(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bounty = Decimal(request.POST["bounty"])  # Convert to Decimal

        # ✅ Ensure user has a profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if user_profile.balance < bounty:
            messages.error(request, "You do not have enough SwishCoins to set this bounty.")
            return redirect("ask_question")

        # Deduct bounty from user balance
        user_profile.balance -= bounty
        user_profile.save()

        # Save the question
        question = Question.objects.create(
            user=request.user,
            title=title,
            description=description,
            bounty=bounty
        )

        return redirect("view_question", question_id=question.id)

    return render(request, "ask_question.html")


@login_required
def user_balances(request):
    users = UserProfile.objects.all().order_by("-balance")  # Sort by highest balance
    return render(request, "users.html", {"users": users})


def user_list(request):
    users = User.objects.all()
    user_data = [
        {
            "username": user.username,
            "balance": getattr(user, 'userprofile', None) and user.userprofile.balance or "No Profile"
        }
        for user in users
    ]
    return render(request, "user_balances.html", {"users": user_data})


@login_required
def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by("-timestamp")

    return render(request, "view_question.html", {"question": question, "answers": answers})


@login_required
def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by("-votes")

    return render(request, "view_question.html", {
        "question": question,
        "answers": answers
    })


@login_required
def post_answer(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Question, id=question_id)
        content = request.POST.get("content")

        if content:
            Answer.objects.create(user=request.user, question=question, content=content)

        return redirect("view_question", question_id=question.id)

    return redirect("list_questions")  # Redirects if accessed improperly


@login_required
def vote_answer(request):
    if request.method == "POST":
        answer_id = request.POST.get("answer_id")
        vote_type = request.POST.get("vote_type")  # "upvote" or "downvote"

        answer = get_object_or_404(Answer, id=answer_id)

        # Prevent users from voting more than once
        if request.user == answer.user:
            return JsonResponse({"error": "You cannot vote on your own answer!"}, status=400)

        if vote_type == "upvote":
            answer.votes += 1
        elif vote_type == "downvote":
            answer.votes -= 1

        answer.save()
        return JsonResponse({"message": "Vote recorded successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def reward_best_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.user:
        return JsonResponse({"error": "Only the question owner can reward the best answer."}, status=403)

    answer_id = request.POST.get("answer_id")
    answer = get_object_or_404(Answer, id=answer_id, question=question)

    if question.bounty > 0:
        # Transfer bounty to answer's author
        answer_owner = UserProfile.objects.get(user=answer.user)
        answer_owner.balance += question.bounty
        answer_owner.save()

        # Reset question bounty to 0
        question.bounty = 0
        question.save()

        Transaction.objects.create(
            sender=question.user,
            receiver=answer.user,
            amount=question.bounty,
            mined=False
        )

        return redirect("view_question", question_id=question.id)

    return JsonResponse({"error": "No bounty to reward!"}, status=400)


@login_required
def ask_question(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        bounty = request.POST.get("bounty", 0)

        user_profile = request.user.userprofile
        if user_profile.balance >= float(bounty):
            user_profile.balance -= float(bounty)
            user_profile.save()

            Question.objects.create(user=request.user, title=title, description=description, bounty=bounty)
            return redirect("view_questions")

        return render(request, "ask_question.html", {"error": "Insufficient balance"})

    return render(request, "ask_question.html")


@login_required
def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by("-votes")  # Ensure answers are fetched

    return render(request, "view_question.html", {
        "question": question,
        "answers": answers
    })


def list_questions(request):
    questions = Question.objects.all()
    return render(request, "list_questions.html", {"questions": questions})


def answer_question(request, question_id):
    return render(request, "answer_question.html", {"question_id": question_id})


def user_balances(request):
    users = UserProfile.objects.all()
    return render(request, "users.html", {"users": users})


@login_required
def transactions(request):
    all_transactions = Transaction.objects.all().order_by("-timestamp")
    return render(request, "transactions.html", {"transactions": all_transactions})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if not UserProfile.can_create_new_coins(100):  # 100 SwishCoins per user
                return render(request, "register.html", {"form": form, "error": "SwishCoin supply limit reached!"})

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            UserProfile.objects.create(user=user, balance=100.0)  # Assign initial balance
            login(request, user)
            return redirect("profile")
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        print("POST request received")  # Debugging print
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("User logged in successfully")  # Debugging print
                return redirect("profile")  # Change 'profile' to the correct post-login page
            else:
                print("Authentication failed")  # Debugging print
        else:
            print("Form is invalid")  # Debugging print

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    total_supply = UserProfile.total_supply()
    return render(request, "profile.html", {"profile": profile, "total_supply": total_supply})


from django.shortcuts import render, get_object_or_404
from .models import Question


def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "view_question.html", {"question": question})
