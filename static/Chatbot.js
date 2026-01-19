const chatBox = document.getElementById("chat");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

let step = 0;
let formData = {};

// -------------------------
// Add messages to chat
// -------------------------
function addMessage(msg, type = "bot", isHTML = false) {
    const p = document.createElement("p");
    p.className = type === "bot" ? "bot-msg" : "user-msg";
    if (isHTML) {
        p.innerHTML = msg;
    } else {
        p.textContent = msg;
    }
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// -------------------------
// Typing indicator helpers
// -------------------------
function createTypingElement() {
    const div = document.createElement("div");
    div.className = "typing-indicator";
    div.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
    return div;
}

let typingElem = null;

function showTyping() {
    if (typingElem) return;
    typingElem = createTypingElement();
    chatBox.appendChild(typingElem);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
    if (!typingElem) return;
    typingElem.remove();
    typingElem = null;
}

/**
 * Add bot message with typing simulation.
 */
function addBotMessage(msg, delay = 700, cb = null) {
    showTyping();
    const computed = Math.min(1500, Math.max(500, delay + Math.min(500, msg.length * 4)));
    setTimeout(() => {
        hideTyping();
        addMessage(msg, "bot", true);
        if (typeof cb === "function") cb();
    }, computed);
}

// -------------------------
// Conversation end helpers
// -------------------------
function disableInput(disabled) {
    userInput.disabled = disabled;
    sendBtn.disabled = disabled;
    const inputArea = document.getElementById("input-area");
    if (disabled) {
        inputArea.classList.add("disabled");
        userInput.placeholder = "Conversation ended. Use Restart to begin again.";
    } else {
        inputArea.classList.remove("disabled");
        userInput.placeholder = "Type your answer...";
    }
}

function addRestartButton() {
    const existing = document.getElementById("restart-container");
    if (existing) existing.remove();

    const container = document.createElement("div");
    container.id = "restart-container";
    container.style.marginTop = "12px";

    const btn = document.createElement("button");
    btn.className = "option-btn restart-btn";
    btn.textContent = "Restart Conversation";
    btn.addEventListener("click", () => {
        restartConversation();
        container.remove();
    });

    container.appendChild(btn);
    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function restartConversation() {
    step = 0;
    formData = {};
    chatBox.innerHTML = "";
    typingElem = null;
    disableInput(false);
    addBotMessage("Hello, I’m Jenny your super agent that will guide you.", 800, () => {
        addBotMessage("May I know your name?");
    });
}

// -------------------------
// Add option buttons
// -------------------------
function addOptions(options) {
    const div = document.createElement("div");
    div.className = "options-container";

    options.forEach(option => {
        const btn = document.createElement("button");
        btn.className = "option-btn";
        btn.textContent = option;
        btn.addEventListener("click", () => {
            nextStep(option);
            div.remove();
        });
        div.appendChild(btn);
    });

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// -------------------------
// Calculate user age
// -------------------------
function calculateAge(dob) {
    const [d, m, y] = dob.split("/").map(Number);
    const birth = new Date(y, m - 1, d);
    const today = new Date();
    let age = today.getFullYear() - birth.getFullYear();
    if (
        today.getMonth() < birth.getMonth() ||
        (today.getMonth() === birth.getMonth() && today.getDate() < birth.getDate())
    ) age--;
    return age;
}

// -------------------------
// Chatbot flow
// -------------------------
function nextStep(input) {
    input = input.trim();

    // STEP 0 – NAME
    if (step === 0) {
        if (!input) return alert("Please enter your name");
        formData.name = input;
        addMessage(input, "user");
        step++;

        addBotMessage(`Hello ${input}, let’s get to know you better.`, 700, () => {
            addBotMessage("May I know your date of birth? (DD/MM/YYYY)");
        });
    }

    // STEP 1 – DOB
    else if (step === 1) {
        if (!/^\d{2}\/\d{2}\/\d{4}$/.test(input)) {
            return alert("Invalid format of Date of birth");
        }

       const age = calculateAge(input);
       if (age < 18 || age > 80) {
        return alert("Sorry, only users aged between 18 and 80 can use this chatbot.");
    }


        formData.dob = input;
        addMessage(input, "user");

        addBotMessage(`At age ${age}, planning for your child’s future is a smart move! 🎓`, 700, () => {
            addBotMessage("May I know how old is your little one?<br>(Child’s age must be between 1 and 17 years old 😊)");
        });

        step++;
    }

    // STEP 2 – CHILD AGE
    else if (step === 2) {
        const childAge = parseInt(input);
        if (isNaN(childAge) || childAge < 1 || childAge > 17) {
            return alert("Oops, a child’s age should be between 1 and 17 years.");
        }

        formData.child_age = childAge;
        addMessage(input, "user");
        step++;
        addBotMessage("Thinking about your child’s future is exciting! 🧒👧", 700, () => {
            addBotMessage("How much would you like to save each month? (RM)");
        });
    }

    // STEP 3 – MONTHLY CONTRIBUTION
    else if (step === 3) {
        const budget = parseFloat(input);
        if (isNaN(budget) || budget <= 0) {
            return alert("Please enter a valid amount");
        }

        formData.budget = budget;
        addMessage(input, "user");
        step++;
        addBotMessage("Just curious! Do you currently have any savings for your child’s education? 🧒👧", 700, () => {
            addOptions([
                "None",
                "RM1000–RM5000",
                "RM5000–RM8000",
                "More than RM8000"
            ]);
        });
    }

// STEP 4 – CURRENT SAVINGS
else if (step === 4) {
    formData.education_savings = input || "None";
    addMessage(input, "user");
    step++;

    if (input === "None") {
        // Show first: tips message
        addBotMessage("No worries! Let’s work together to start saving for your child’s future. I’ll share some tips to help you get started.", 700, () => {
            // Then show: phone number request
            addBotMessage("Please enter your phone number so we can provide you with updates from time to time on suitable offers and packages.");
        });
    } else {
        addBotMessage(`That’s great! You’ve already started saving (${input}).`, 700, () => {
            addBotMessage("Please enter your phone number so we can provide you with updates from time to time on suitable offers and packages.");
        });
    }
}


    // STEP 5 – PHONE
    else if (step === 5) {
        if (!/^(\+60|60)[0-9]{9}$|^01[0-9]{8}$/.test(input)) {
            return alert("Invalid Malaysian phone number.");
        }

        formData.phone = input;
        addMessage(input, "user");
        step++;
        addBotMessage("Please type your email address, we will send you an email summary of our conversation for your reference");
    }

    // STEP 6 – EMAIL + CALCULATION
    else if (step === 6) {
        if (!/^[\w\.-]+@[\w\.-]+\.\w+$/.test(input)) {
            return alert("Invalid format of Email");
        }

        formData.email = input;
        addMessage(input, "user");

        showTyping();
        fetch("/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        })
        .then(res => res.json())
        .then(data => {
            hideTyping();

            // Single bubble for Education Fund
            const fundMsg = `
📘 Projected Education Fund<br><br>
Years until university: ${data.years_to_uni} years<br>
Annual contribution: RM ${data.annual_contribution.toFixed(2)}<br><br>
Estimated savings at age 18:<br>
• 6% return: RM ${data.fv_6.toFixed(2)}<br>
• 8% return: RM ${data.fv_8.toFixed(2)}<br>
• 10% return: RM ${data.fv_10.toFixed(2)}
`;
            addBotMessage(fundMsg, 0, () => {
                step++;
                addBotMessage("Would you like to learn more about planning your child’s education and future?", 700, () => {
                    addOptions(["Yes", "No"]);
                });
            });
        })
        .catch(err => {
            hideTyping();
            console.error(err);
            addBotMessage("Sorry, something went wrong. Please try again later.");
        });
    }

    // STEP 7 – YES / NO
    else if (step === 7) {
        addMessage(input, "user");

        // Single bubble for Thank You + T&C
        const thankMsg1 = `Great! Thank you for signing up. We will contact you soon 😊<br>
Subject to terms and conditions of approved policy after recommendation by authorised representatives.`;
        addBotMessage(thankMsg1, 800);

        // Single bubble for Contact Info
        const thankMsg2 = `Thank you for contacting us.<br>
Feel free to reach out to us if you would like more information at <a href="https://wa.me/60168357258" target="_blank">016-835 7258</a>.`;

        setTimeout(() => {
            addBotMessage(thankMsg2, 800, () => {
                disableInput(true);
                addRestartButton();
            });
        }, 1600);

        step++;
    }

    userInput.value = "";
}

// -------------------------
// Event listeners
// -------------------------
sendBtn.addEventListener("click", () => nextStep(userInput.value));
userInput.addEventListener("keypress", e => {
    if (e.key === "Enter") nextStep(userInput.value);
});

// -------------------------
// Initial greeting
// -------------------------
addBotMessage("Hello, I’m Jenny your super agent that will guide you.", 800, () => {
    addBotMessage("May I know your name?");
});
