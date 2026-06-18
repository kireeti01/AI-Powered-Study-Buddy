"""
AI Study Buddy - Main Streamlit Application
Production-ready educational AI assistant for students
"""

import streamlit as st
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Config, STREAMLIT_CONFIG, ERROR_MESSAGES
from src.modules.topic_explainer import TopicExplainer
from src.modules.notes_summarizer import NotesSummarizer
from src.modules.quiz_generator import QuizGenerator
from src.modules.flashcard_generator import FlashcardGenerator
from src.modules.study_planner import StudyPlanner
from src.modules.qa_engine import QAEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    page_icon=STREAMLIT_CONFIG["page_icon"],
    layout=STREAMLIT_CONFIG["layout"],
    initial_sidebar_state=STREAMLIT_CONFIG["initial_sidebar_state"]
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.25rem;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 0.25rem;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)


class StreamlitApp:
    """Main Streamlit application class"""

    def __init__(self):
        """Initialize Streamlit app and modules"""
        self.initialize_session_state()
        self.load_modules()

    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if "initialized" not in st.session_state:
            st.session_state.initialized = True
            st.session_state.quiz_responses = []
            st.session_state.current_quiz = None
            st.session_state.flashcards = None
            st.session_state.qa_context_loaded = False

    def load_modules(self):
        """Load all AI modules"""
        try:
            self.topic_explainer = TopicExplainer()
            self.notes_summarizer = NotesSummarizer()
            self.quiz_generator = QuizGenerator()
            self.flashcard_generator = FlashcardGenerator()
            self.study_planner = StudyPlanner()
            self.qa_engine = QAEngine()
            logger.info("✅ All modules loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load modules: {str(e)}")
            st.error(f"❌ Failed to initialize: {str(e)}")
            st.stop()

    def show_home(self):
        """Display home page"""
        st.markdown("<div class='main-header'>", unsafe_allow_html=True)
        st.title("📚 AI Study Buddy")
        st.markdown(
            "Your personal AI-powered learning companion | Master any subject efficiently",
            help="Powered by Google Gemini API"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.write("---")

        # Feature overview
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div class='feature-card'>
                    <h3>💡 Topic Explainer</h3>
                    <p>Get AI-powered explanations in simple language with real-world examples.</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class='feature-card'>
                    <h3>📝 Notes Summarizer</h3>
                    <p>Upload documents and get concise summaries with key points highlighted.</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class='feature-card'>
                    <h3>🎯 Quiz Generator</h3>
                    <p>Create interactive quizzes to test your knowledge on any topic.</p>
                </div>
            """, unsafe_allow_html=True)

        st.write("")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div class='feature-card'>
                    <h3>🃏 Flashcards</h3>
                    <p>Generate smart flashcards for efficient spaced learning.</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class='feature-card'>
                    <h3>📅 Study Planner</h3>
                    <p>Get personalized study schedules optimized for your exam date.</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class='feature-card'>
                    <h3>❓ Ask Questions</h3>
                    <p>Ask questions about your notes and get context-aware answers.</p>
                </div>
            """, unsafe_allow_html=True)

        st.write("---")

        # Quick start guide
        st.subheader("🚀 Quick Start")

        with st.expander("How to get started?", expanded=True):
            st.markdown("""
            1. **Select a feature** from the sidebar
            2. **Enter your topic** or **upload a file**
            3. **Configure options** as needed
            4. **Click the action button** to generate content
            5. **Download or review** your results

            **Tips:**
            - Use specific topics for better results
            - Keep questions clear and focused
            - Try different difficulty levels
            - Download flashcards for offline study
            """)

    def show_topic_explainer(self):
        """Display Topic Explainer"""
        st.header("💡 Topic Explainer")
        st.write("Get AI-powered explanations of any topic in simple, beginner-friendly language.")

        col1, col2 = st.columns([3, 1])
        with col1:
            topic = st.text_input(
                "Enter a topic to explain:",
                placeholder="e.g., Photosynthesis, Machine Learning, Quantum Physics",
                help="Enter any topic you want to understand"
            )

        with col2:
            difficulty = st.selectbox(
                "Difficulty Level:",
                ["beginner", "intermediate", "advanced"],
                index=0
            )

        col1, col2 = st.columns(2)
        with col1:
            include_examples = st.checkbox("Include Examples", value=True)
        with col2:
            include_applications = st.checkbox("Include Applications", value=True)

        if st.button("📚 Explain Topic", use_container_width=True, key="explain_btn"):
            if not topic.strip():
                st.error("❌ Please enter a topic")
            else:
                with st.spinner(f"🤔 Explaining '{topic}'..."):
                    try:
                        result = self.topic_explainer.explain_topic(
                            topic=topic,
                            difficulty=difficulty,
                            include_examples=include_examples,
                            include_applications=include_applications
                        )

                        st.success("✅ Explanation generated!")

                        st.markdown("### Full Explanation")
                        st.write(result.get("full_explanation", ""))

                        if "key_phrases" in result and result["key_phrases"]:
                            st.markdown("### 🔑 Key Phrases")
                            for phrase in result["key_phrases"]:
                                st.write(f"• {phrase}")

                        st.download_button(
                            label="📥 Download Explanation",
                            data=result.get("full_explanation", ""),
                            file_name=f"{topic.replace(' ', '_')}_explanation.txt",
                            mime="text/plain"
                        )

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        with st.expander("🔧 Advanced Options"):
            if st.button("Compare Topics"):
                st.info("Feature coming soon!")

            if st.button("Step-by-Step Breakdown"):
                st.info("Feature coming soon!")

    def show_notes_summarizer(self):
        """Display Notes Summarizer"""
        st.header("📝 Notes Summarizer")
        st.write("Upload your study materials and get concise summaries with key points.")

        uploaded_file = st.file_uploader(
            "Upload your notes (PDF or TXT):",
            type=["pdf", "txt"],
            help="Upload documents to summarize"
        )

        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                summary_length = st.selectbox(
                    "Summary Length:",
                    ["short", "medium", "long"],
                    index=1,
                    help="Short (50-100 words), Medium (200-300 words), Long (400-500 words)"
                )

            with col2:
                include_keypoints = st.checkbox("Include Key Points", value=True)

            if st.button("📖 Summarize", use_container_width=True, key="summarize_btn"):
                with st.spinner("📄 Processing your document..."):
                    try:
                        temp_path = Path(f"./temp/{uploaded_file.name}")
                        temp_path.parent.mkdir(exist_ok=True)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        result = self.notes_summarizer.summarize_file(
                            temp_path,
                            length=summary_length,
                            include_keypoints=include_keypoints
                        )

                        st.success("✅ Summary generated!")

                        st.markdown("### 📋 Summary")
                        st.write(result.get("summary", ""))

                        if "key_points" in result and result["key_points"]:
                            st.markdown("### 🎯 Key Points")
                            for point in result["key_points"]:
                                st.write(f"• {point}")

                        if "keywords" in result and result["keywords"]:
                            st.markdown("### 🔑 Important Keywords")
                            keywords_str = ", ".join(result["keywords"])
                            st.write(keywords_str)

                        with st.expander("📊 Document Statistics"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Original Length", f"{result.get('original_length', 0)} chars")
                            with col2:
                                st.metric("Summary Length", f"{result.get('summary_length', 0)} chars")
                            with col3:
                                ratio = result.get('compression_ratio', 0)
                                st.metric("Compression Ratio", f"{ratio:.1%}")

                        st.download_button(
                            label="📥 Download Summary",
                            data=result.get("summary", ""),
                            file_name=f"{uploaded_file.name.split('.')[0]}_summary.txt",
                            mime="text/plain"
                        )

                        temp_path.unlink()

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Upload a file to get started")

    def show_quiz_generator(self):
        """Display Quiz Generator"""
        st.header("🎯 Quiz Generator")
        st.write("Create interactive quizzes to test your knowledge.")

        tab1, tab2 = st.tabs(["From Topic", "From Notes"])

        with tab1:
            topic = st.text_input("Enter a topic for quiz:")

            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.slider(
                    "Number of Questions:",
                    min_value=5,
                    max_value=20,
                    value=10,
                    step=1
                )

            with col2:
                difficulty = st.selectbox(
                    "Difficulty:",
                    ["easy", "medium", "hard"],
                    index=1
                )

            question_types = st.multiselect(
                "Question Types:",
                ["mcq", "true_false", "short_answer"],
                default=["mcq", "true_false"]
            )

            if st.button("✅ Generate Quiz", use_container_width=True, key="quiz_btn"):
                if not topic.strip():
                    st.error("❌ Please enter a topic")
                elif not question_types:
                    st.error("❌ Select at least one question type")
                else:
                    with st.spinner(f"🤔 Creating quiz on '{topic}'..."):
                        try:
                            quiz = self.quiz_generator.generate_quiz(
                                topic=topic,
                                num_questions=num_questions,
                                question_types=question_types,
                                difficulty=difficulty
                            )

                            st.session_state.current_quiz = quiz
                            st.success("✅ Quiz created!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

        with tab2:
            uploaded_file = st.file_uploader(
                "Upload notes for quiz:",
                type=["pdf", "txt"],
                key="quiz_file"
            )

            if uploaded_file:
                num_questions = st.slider(
                    "Number of Questions:",
                    min_value=5,
                    max_value=20,
                    value=10,
                    step=1,
                    key="quiz_from_file_slider"
                )

                if st.button("✅ Generate Quiz from File", use_container_width=True, key="quiz_file_btn"):
                    with st.spinner("🤔 Creating quiz from notes..."):
                        try:
                            temp_path = Path(f"./temp/{uploaded_file.name}")
                            temp_path.parent.mkdir(exist_ok=True)
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            quiz = self.quiz_generator.generate_quiz_from_notes(
                                temp_path,
                                num_questions=num_questions
                            )

                            st.session_state.current_quiz = quiz
                            st.success("✅ Quiz created!")
                            st.rerun()

                            temp_path.unlink()

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

        # Display quiz if one is loaded
        if st.session_state.current_quiz:
            st.write("---")
            self.display_quiz(st.session_state.current_quiz)

    def display_quiz(self, quiz: dict):
        """Display interactive quiz"""
        questions = quiz.get("questions", [])

        if not questions:
            st.warning("No questions in quiz")
            return

        st.subheader(quiz.get("quiz_title", "Quiz"))

        responses = []
        for i, q in enumerate(questions, 1):
            st.markdown(f"### Question {i}")
            st.write(q.get("question", ""))

            if q.get("type") == "mcq":
                answer = st.radio(
                    "Choose an answer:",
                    q.get("options", []),
                    index=None,
                    key=f"q_{i}"
                )
            elif q.get("type") == "true_false":
                answer = st.selectbox(
                    "Choose an answer:",
                    ["True", "False"],
                    index=None,
                    key=f"q_{i}"
                )
            else:  # short_answer
                answer = st.text_input(
                    "Your answer:",
                    key=f"q_{i}"
                )

            responses.append({
                "question_id": i,
                "answer": answer,
                "is_correct": answer == q.get("correct_answer")
            })

            st.write("---")

        if st.button("📊 Submit Quiz", use_container_width=True):
            score = self.quiz_generator.calculate_quiz_score(responses)

            st.success("✅ Quiz Complete!")
            st.metric("Your Score", f"{score['percentage']}%", delta=None)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Correct", score['correct_answers'])
            with col2:
                st.metric("Incorrect", score['incorrect_answers'])
            with col3:
                st.metric("Grade", score['grade'])
            with col4:
                st.write(score['performance'])

    def show_flashcard_generator(self):
        """Display Flashcard Generator"""
        st.header("🃏 Flashcard Generator")
        st.write("Create smart flashcards for efficient learning.")

        tab1, tab2 = st.tabs(["From Topic", "From Notes"])

        with tab1:
            topic = st.text_input("Enter a topic for flashcards:")
            num_cards = st.slider("Number of Flashcards:", 5, 50, 15, 1)
            card_type = st.selectbox("Card Type:", ["concept", "definition", "question", "scenario"])

            if st.button("✨ Generate Flashcards", use_container_width=True, key="flashcard_btn"):
                if not topic.strip():
                    st.error("❌ Please enter a topic")
                else:
                    with st.spinner("🤔 Creating flashcards..."):
                        try:
                            result = self.flashcard_generator.generate_flashcards(
                                topic=topic,
                                num_cards=num_cards,
                                card_type=card_type
                            )

                            st.session_state.flashcards = result
                            st.success("✅ Flashcards created!")
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

        with tab2:
            uploaded_file = st.file_uploader(
                "Upload notes for flashcards:",
                type=["pdf", "txt"],
                key="flashcard_file"
            )

            if uploaded_file:
                num_cards = st.slider(
                    "Number of Flashcards:",
                    5, 50, 15, 1,
                    key="flashcard_file_slider"
                )

                if st.button("✨ Generate Flashcards from File", use_container_width=True, key="flashcard_file_btn"):
                    with st.spinner("🤔 Creating flashcards..."):
                        try:
                            temp_path = Path(f"./temp/{uploaded_file.name}")
                            temp_path.parent.mkdir(exist_ok=True)
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            result = self.flashcard_generator.generate_flashcards_from_notes(
                                temp_path,
                                num_cards=num_cards
                            )

                            st.session_state.flashcards = result
                            st.success("✅ Flashcards created!")
                            st.rerun()

                            temp_path.unlink()

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

        # Display flashcards
        if st.session_state.flashcards:
            st.write("---")
            self.display_flashcards(st.session_state.flashcards)

    def display_flashcards(self, flashcard_data: dict):
        """Display flashcards in interactive mode"""
        cards = flashcard_data.get("cards", [])
        st.subheader(f"📚 {len(cards)} Flashcards Created")

        if not cards:
            st.warning("No flashcards created")
            return

        col1, col2 = st.columns([3, 1])
        with col1:
            current_card = st.slider("Flashcard:", 1, len(cards), 1)

        card = cards[current_card - 1]

        st.markdown("---")
        st.markdown(f"### Card {current_card}/{len(cards)}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📖 Front")
            st.write(card.get("front", ""))

        with col2:
            if st.button("👁️ Show Answer", key=f"show_{current_card}"):
                st.markdown("#### ✅ Back")
                st.write(card.get("back", ""))

        if card.get("memory_aid"):
            st.markdown("#### 💡 Memory Aid")
            st.write(card.get("memory_aid"))

        st.markdown("---")

        st.subheader("📥 Export Flashcards")

        col1, col2, col3 = st.columns(3)

        with col1:
            anki_content = self.flashcard_generator.export_to_anki(cards)
            st.download_button(
                label="📱 Anki Format",
                data=anki_content,
                file_name="flashcards.txt",
                mime="text/plain"
            )

        with col2:
            csv_content = self.flashcard_generator.export_to_csv(cards)
            st.download_button(
                label="📊 CSV Format",
                data=csv_content,
                file_name="flashcards.csv",
                mime="text/csv"
            )

        with col3:
            json_content = self.flashcard_generator.export_to_json(cards)
            st.download_button(
                label="📄 JSON Format",
                data=json_content,
                file_name="flashcards.json",
                mime="application/json"
            )

        with st.expander("📅 Recommended Study Schedule"):
            schedule = self.flashcard_generator.get_spaced_repetition_schedule(len(cards))
            for day, info in schedule["schedule"].items():
                st.write(f"**{day}**: {info['cards_to_review']} cards ({info['description']})")

    def show_study_planner(self):
        """Display Study Planner"""
        st.header("📅 Study Planner")
        st.write("Create a personalized study schedule optimized for your success.")

        col1, col2 = st.columns(2)

        with col1:
            exam_date = st.date_input(
                "Exam Date:",
                help="When is your exam?"
            )

        with col2:
            daily_hours = st.number_input(
                "Daily Study Hours:",
                min_value=1.0,
                max_value=8.0,
                value=2.0,
                step=0.5
            )

        topics = st.multiselect(
            "Topics to Study:",
            ["Mathematics", "Physics", "Chemistry", "Biology", "History", "Literature", "Custom"],
            default=["Mathematics"]
        )

        if "Custom" in topics:
            custom_topics = st.text_area(
                "Enter custom topics (one per line):",
                height=100
            ).split("\n")
            topics = [t.strip() for t in custom_topics if t.strip()]

        learning_style = st.selectbox(
            "Learning Style:",
            ["visual", "auditory", "kinesthetic", "mixed"]
        )

        if st.button("📚 Create Study Schedule", use_container_width=True, key="planner_btn"):
            if not topics:
                st.error("❌ Please select at least one topic")
            else:
                with st.spinner("🤔 Creating your personalized study schedule..."):
                    try:
                        schedule = self.study_planner.create_study_schedule(
                            exam_date=exam_date.strftime("%Y-%m-%d"),
                            topics=topics,
                            daily_hours=daily_hours,
                            learning_style=learning_style
                        )

                        st.success("✅ Study schedule created!")

                        st.markdown("### 📋 Your Study Schedule")
                        st.write(schedule.get("schedule", ""))

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Days Until Exam", schedule.get("days_until_exam", 0))
                        with col2:
                            st.metric("Daily Hours", f"{schedule.get('daily_hours', 0)}")
                        with col3:
                            st.metric("Total Hours", f"{schedule.get('total_study_hours', 0):.1f}")
                        with col4:
                            st.metric("Topics", len(schedule.get("topics", [])))

                        if schedule.get("milestones"):
                            st.markdown("### 🎯 Milestones")
                            for milestone in schedule["milestones"]:
                                with st.expander(f"Day {milestone['day']}: {milestone['topic']}"):
                                    st.write(f"**Goal**: {milestone['goal']}")
                                    st.write(f"**Deliverable**: {milestone['deliverable']}")

                        st.download_button(
                            label="📥 Download Schedule",
                            data=schedule.get("schedule", ""),
                            file_name="study_schedule.txt",
                            mime="text/plain"
                        )

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    def show_qa_engine(self):
        """Display Q&A Engine"""
        st.header("❓ Ask Questions from Notes")
        st.write("Upload your study materials and ask context-aware questions.")

        # Initialize QA state
        if "qa_loaded" not in st.session_state:
            st.session_state.qa_loaded = False

        if "qa_file_path" not in st.session_state:
            st.session_state.qa_file_path = None

        uploaded_file = st.file_uploader(
            "Upload study material (PDF or TXT):",
            type=["pdf", "txt"],
            key="qa_file"
        )

        if uploaded_file:
            if st.button("📚 Load Material", use_container_width=True):
                with st.spinner("📖 Loading material..."):
                    try:
                        temp_dir = Path("./temp")
                        temp_dir.mkdir(exist_ok=True)
                        temp_path = temp_dir / uploaded_file.name

                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        self.qa_engine.load_context_from_file(temp_path)

                        st.session_state.qa_loaded = True
                        st.session_state.qa_file_path = str(temp_path)

                        st.success("✅ Material loaded successfully!")

                        stats = self.qa_engine.get_context_summary()
                        with st.expander("📊 Material Statistics"):
                            st.json(stats)

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        if st.session_state.qa_loaded:
            st.divider()
            st.subheader("💬 Ask Your Questions")

            question = st.text_input(
                "What would you like to know?",
                placeholder="Example: Explain my project experience"
            )

            answer_length = st.selectbox(
                "Answer Length:",
                ["short", "medium", "long"],
                index=1
            )

            if st.button("🔍 Get Answer", use_container_width=True):
                if not question.strip():
                    st.error("❌ Please enter a question")
                else:
                    with st.spinner("🤔 Finding answer..."):
                        try:
                            self.qa_engine.load_context_from_file(
                                Path(st.session_state.qa_file_path)
                            )

                            result = self.qa_engine.answer_question(
                                question=question,
                                answer_length=answer_length
                            )

                            st.success("✅ Answer found!")
                            st.markdown("### 📖 Answer")
                            st.write(result.get("answer", result))

                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Upload study material and click Load Material first")

    def run(self):
        """Run the Streamlit application"""
        # Sidebar navigation
        with st.sidebar:
            st.title("📚 AI Study Buddy")
            st.write("---")

            page = st.radio(
                "Navigate to:",
                [
                    "🏠 Home",
                    "💡 Topic Explainer",
                    "📝 Notes Summarizer",
                    "🎯 Quiz Generator",
                    "🃏 Flashcard Generator",
                    "📅 Study Planner",
                    "❓ Ask Questions"
                ]
            )

            st.write("---")
            st.caption("Powered by Groq | Built by Yogendra")
            st.caption(f"© {datetime.now().year} AI Study Buddy")

        # Route to correct page
        if page == "🏠 Home":
            self.show_home()
        elif page == "💡 Topic Explainer":
            self.show_topic_explainer()
        elif page == "📝 Notes Summarizer":
            self.show_notes_summarizer()
        elif page == "🎯 Quiz Generator":
            self.show_quiz_generator()
        elif page == "🃏 Flashcard Generator":
            self.show_flashcard_generator()
        elif page == "📅 Study Planner":
            self.show_study_planner()
        elif page == "❓ Ask Questions":
            self.show_qa_engine()


def main():
    """Main entry point"""
    app = StreamlitApp()
    app.run()


if __name__ == "__main__":
    main()
