let TIME_PER_QUESTION = 60;   // ⏱️ 1 minute per question
let timeLeft = TIME_PER_QUESTION;
let timer = null;
let scores = [];
let interviewActive = false;

// ---------------- START INTERVIEW ----------------
function startInterview() {
    const resume = document.getElementById("resume").value.trim();
    const jd = document.getElementById("jd").value.trim();

    if (!resume || !jd) {
        alert("Please paste Resume and Job Description first");
        return;
    }

    fetch("http://127.0.0.1:5000/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume, jd })
    })
    .then(res => res.json())
    .then(() => {
        interviewActive = true;
        scores = [];
        document.getElementById("result").innerHTML = "";
        document.getElementById("interview-box").classList.remove("hidden");
        fetchQuestion();
    })
    .catch(() => {
        alert("Backend not reachable. Is Flask running?");
    });
}

// ---------------- FETCH QUESTION ----------------
function fetchQuestion() {
    if (!interviewActive) return;

    document.getElementById("answer").value = "";
    document.getElementById("timer").innerText = "";

    fetch("http://127.0.0.1:5000/question")
        .then(res => res.json())
        .then(data => {
            if (!data.question || data.question.includes("Interview")) {
                showFinalResult();
                return;
            }

            document.getElementById("question").innerText = data.question;

            // 🎙️ Voice Interview
            if ("speechSynthesis" in window) {
                speakQuestion(data.question);
            }

            startTimer();
        });
}

// ---------------- TIMER ----------------
function startTimer() {
    clearInterval(timer);
    timeLeft = TIME_PER_QUESTION;

    timer = setInterval(() => {
        document.getElementById("timer").innerText =
            `⏱️ Time Left: ${timeLeft} sec`;

        timeLeft--;

        if (timeLeft < 0) {
            clearInterval(timer);
            submitAnswer(true); // auto-submit (timeout)
        }
    }, 1000);
}

// ---------------- SUBMIT ANSWER ----------------
function submitAnswer(timeout = false) {
    clearInterval(timer);

    const ans = timeout ? "" : document.getElementById("answer").value;

    fetch("http://127.0.0.1:5000/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            answer: ans,
            time: timeLeft
        })
    })
    .then(res => res.json())
    .then(data => {
        scores.push(data.accuracy);

        document.getElementById("result").innerHTML = `
            <div class="result-card">
                <div class="score">
                    <div class="num">${data.accuracy}%</div>
                    <div class="label">Accuracy</div>
                </div>
                <div class="feedback">
                    <strong>${data.badge}</strong><br>
                    Question Score: ${data.score}
                </div>
            </div>
        `;

        // ✅ INTERVIEW COMPLETED
        if (data.completed) {
            interviewActive = false;

            localStorage.setItem("interviewResult", JSON.stringify({
                accuracy: data.accuracy,
                badge: data.badge,
                attempts: data.attempts,
                scores
            }));

            setTimeout(() => {
                window.location.href = "result.html";
            }, 1200);
        } else {
            fetchQuestion();
        }
    });
}

// ---------------- RESTART ----------------
function restartInterview() {
    interviewActive = false;
    scores = [];
    clearInterval(timer);

    document.getElementById("result").innerHTML = "";
    document.getElementById("interview-box").classList.add("hidden");
}

// ---------------- VOICE ----------------
function speakQuestion(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 0.9;
    speech.pitch = 1;
    speech.volume = 1;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);
}
