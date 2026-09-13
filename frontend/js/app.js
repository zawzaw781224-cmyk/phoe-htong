const API_URL = "http://127.0.0.1:8000";

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

const status = document.getElementById("status");
const answerBox = document.getElementById("answer");
const recordButton = document.getElementById("recordButton");

const recognition = new SpeechRecognition();

recognition.lang = "my-MM";
recognition.continuous = false;
recognition.interimResults = false;

let isListening = false;
// ==============================
// Wake Word Check
// ==============================

// ==============================
// Wake Word Check
// ==============================

function hasWakeWord(text) {

    const normalizedText = text
        .replace(/\s+/g, "")
        .toLowerCase();

    const wakeWords = [
        "ဖိုးထောင်",
        "ထူထောင်"
    ];

    return wakeWords.some(word =>
        normalizedText.includes(word)
    );
}


// ==============================
// Button
// ==============================

recordButton.addEventListener("click", () => {

    if (isListening) {
        recognition.stop();
        return;
    }

    recognition.start();

});


// ==============================
// Speech Start
// ==============================

recognition.onstart = () => {

    isListening = true;

    recordButton.textContent = "⏹️ ရပ်မယ်";
    status.textContent = "🎤 ဖိုးထောင် နားထောင်နေပါတယ်...";

};


// ==============================
// Speech Result
// ==============================

recognition.onresult = async (event) => {

    const text = event.results[0][0].transcript;

    console.log("🗣 မင်းပြောတာ:", text);


    // ==============================
    // Check Wake Word
    // ==============================

    if (!hasWakeWord(text)) {

        console.log("❌ Wake Word မပါပါ");

        status.textContent =
            "👂 ဖိုးထောင်ကို ခေါ်ပြီး မေးပါ။";

        answerBox.textContent =
            `မင်း: ${text}\n\nဖိုးထောင်ကို ခေါ်ပြီး မေးပါ။`;

        return;
    }


    console.log("✅ Wake Word တွေ့ပါပြီ");


    // ==============================
    // Remove Wake Word
    // ==============================

    const question = text
    .replace(/ဖိုး\s*ထောင်ရေ?/g, "")
    .replace(/ထူ\s*ထောင်/g, "")
    .trim();


    console.log("❓ မေးခွန်း:", question);


    if (!question) {

        status.textContent =
            "👂 ဟုတ်ကဲ့၊ ဖိုးထောင် နားထောင်နေပါတယ်။";

        answerBox.textContent =
            "ဘာကို သိချင်တာလဲ ပြောပါ။";

        return;
    }


    status.textContent =
        "🧠 ဖိုးထောင် စဉ်းစားနေပါတယ်...";

    answerBox.textContent =
        `မင်း: ${question}`;


    await askAI(question);

};


// ==============================
// Speech End
// ==============================

recognition.onend = () => {

    isListening = false;

    recordButton.textContent = "🎤 ဖိုးထောင်ကို မေးမယ်";

};


// ==============================
// Speech Error
// ==============================

recognition.onerror = (event) => {

    console.error("Speech Error:", event.error);

    isListening = false;

    recordButton.textContent = "🎤 ဖိုးထောင်ကို မေးမယ်";

    status.textContent =
        "❌ အသံနားထောင်ရာမှာ ပြဿနာရှိပါတယ်။";

};


// ==============================
// Send text to Gemini
// ==============================

async function askAI(text) {

    try {

        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text
                })
            }
        );


        if (!response.ok) {
            throw new Error("Chat request failed");
        }


        const data = await response.json();


        console.log("🤖 ဖိုးထောင်:", data.answer);


        answerBox.textContent =
            `မင်း: ${text}\n\nဖိုးထောင်: ${data.answer}`;


        status.textContent =
            "🔊 ဖိုးထောင် ပြောနေပါတယ်...";


        console.log("✅ AI answer ရပါပြီ");
        console.log("➡️ speak() ကို ခေါ်တော့မယ်");

        await speak(data.answer);

        console.log("⬅️ speak() ပြန်ပြီးပါပြီ");


    } catch (error) {

        console.error(error);

        status.textContent =
            "❌ ဖိုးထောင်နဲ့ ချိတ်ဆက်ရာမှာ Error ဖြစ်ပါတယ်။";

    }

}


// ==============================
// Text → Speech
// ==============================

async function speak(text) {
    try {
        console.log("🔊 TTS စတင်:", text);

        status.textContent = "🔊 ဖိုးထောင် ပြောနေပါတယ်...";

        console.log("📡 /tts ကို request ပို့နေပါတယ်...");

        const response = await fetch(
            `${API_URL}/tts`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            }
        );

        console.log("📥 /tts response:", response.status);

        if (!response.ok) {
            throw new Error(`TTS request failed: ${response.status}`);
        }

        const audioBlob = await response.blob();

        console.log(
            "🎵 Audio ရပါပြီ:",
            audioBlob.size,
            "bytes"
        );

        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);

        audio.onplay = () => {
            console.log("▶️ Audio စတင်ဖွင့်နေပါတယ်");
        };

        audio.onended = () => {
            console.log("✅ Audio ပြီးပါပြီ");

            URL.revokeObjectURL(audioUrl);

            status.textContent =
                "🎤 ဖိုးထောင်ကို မေးနိုင်ပါတယ်။";
        };

        audio.onerror = (event) => {
            console.error("❌ Audio playback error:", event);
        };

        console.log("▶️ Audio play() ခေါ်နေပါတယ်...");

        await audio.play();

        console.log("✅ audio.play() အောင်မြင်ပါတယ်");

    } catch (error) {
        console.error("❌ TTS Error:", error);

        status.textContent =
            "❌ ဖိုးထောင် အသံထွက်ရာမှာ Error ဖြစ်ပါတယ်။";
    }
}
