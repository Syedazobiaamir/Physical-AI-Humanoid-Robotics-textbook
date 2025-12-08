import React, { useState, useEffect } from 'react';

interface QuizQuestion {
  id: string;
  text: string;
  options: string[];
  correctAnswer: number;
  explanation?: string;
}

interface Quiz {
  id: string;
  chapterId: string;
  questions: QuizQuestion[];
}

interface ChapterQuizProps {
  chapterId: string;
}

const ChapterQuiz: React.FC<ChapterQuizProps> = ({ chapterId }) => {
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadQuiz();
  }, [chapterId]);

  const loadQuiz = async () => {
    setLoading(true);
    setError(null);

    try {
      // Try to fetch from backend API
      const response = await fetch(`http://localhost:8000/api/v1/quizzes/${chapterId}`);

      if (response.ok) {
        const data = await response.json();
        setQuiz(data);
      } else {
        // Fallback to static quiz data
        setQuiz(getStaticQuiz(chapterId));
      }
    } catch (err) {
      // Use static quiz data as fallback
      setQuiz(getStaticQuiz(chapterId));
    } finally {
      setLoading(false);
    }
  };

  const getStaticQuiz = (chapterId: string): Quiz => {
    // Static quiz data for offline/development use
    const quizzes: Record<string, Quiz> = {
      'week-1-intro': {
        id: 'quiz-week-1',
        chapterId: 'week-1-intro',
        questions: [
          {
            id: 'q1',
            text: 'What middleware technology does ROS2 use for communication?',
            options: ['TCP/IP', 'DDS (Data Distribution Service)', 'HTTP', 'gRPC'],
            correctAnswer: 1,
            explanation: 'ROS2 uses DDS (Data Distribution Service) as its middleware layer, providing real-time and reliable communication.',
          },
          {
            id: 'q2',
            text: 'Which of the following is NOT a core concept in ROS2?',
            options: ['Nodes', 'Topics', 'Databases', 'Services'],
            correctAnswer: 2,
            explanation: 'Databases are not a core ROS2 concept. The core concepts are Nodes, Topics, Services, Actions, and Parameters.',
          },
          {
            id: 'q3',
            text: 'What is the primary advantage of ROS2 over ROS1?',
            options: ['More programming languages', 'Real-time capabilities', 'Larger community', 'More robots supported'],
            correctAnswer: 1,
            explanation: 'ROS2 was designed with real-time capabilities in mind, addressing one of the main limitations of ROS1.',
          },
          {
            id: 'q4',
            text: 'What command is used to list all running nodes in ROS2?',
            options: ['ros2 list nodes', 'ros2 node list', 'ros2 nodes', 'ros2 show nodes'],
            correctAnswer: 1,
            explanation: 'The command "ros2 node list" displays all currently running ROS2 nodes.',
          },
          {
            id: 'q5',
            text: 'In ROS2, what is the recommended distribution for production use as of 2024?',
            options: ['Foxy', 'Galactic', 'Humble', 'Iron'],
            correctAnswer: 2,
            explanation: 'ROS2 Humble is an LTS (Long Term Support) release recommended for production use.',
          },
        ],
      },
    };

    return quizzes[chapterId] || {
      id: `quiz-${chapterId}`,
      chapterId,
      questions: [
        {
          id: 'q1',
          text: 'Sample question for this chapter',
          options: ['Option A', 'Option B', 'Option C', 'Option D'],
          correctAnswer: 0,
          explanation: 'This is a placeholder quiz. Real quiz content will be loaded from the backend.',
        },
      ],
    };
  };

  const handleAnswerSelect = (questionId: string, optionIndex: number) => {
    if (submitted) return;
    setAnswers((prev) => ({
      ...prev,
      [questionId]: optionIndex,
    }));
  };

  const handleSubmit = async () => {
    if (!quiz) return;

    // Calculate score
    let correct = 0;
    quiz.questions.forEach((question) => {
      if (answers[question.id] === question.correctAnswer) {
        correct++;
      }
    });

    const calculatedScore = Math.round((correct / quiz.questions.length) * 100);
    setScore(calculatedScore);
    setSubmitted(true);

    // Try to submit to backend
    try {
      await fetch(`http://localhost:8000/api/v1/quizzes/${chapterId}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          answers: Object.entries(answers).map(([questionId, selectedOption]) => ({
            question_id: questionId,
            selected_option: selectedOption,
          })),
        }),
      });
    } catch (err) {
      // Submission failed, but we still show local results
      console.warn('Failed to submit quiz results to backend');
    }
  };

  const handleReset = () => {
    setAnswers({});
    setSubmitted(false);
    setScore(null);
  };

  if (loading) {
    return (
      <div className="quiz-container">
        <div className="quiz-loading">Loading quiz...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="quiz-container">
        <div className="quiz-error">{error}</div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="quiz-container">
        <div className="quiz-error">No quiz available for this chapter.</div>
      </div>
    );
  }

  return (
    <div className="quiz-container">
      <h3>Chapter Quiz</h3>

      {submitted && score !== null && (
        <div
          className={`quiz-result ${score >= 80 ? 'quiz-result-pass' : 'quiz-result-fail'}`}
        >
          <h4>Your Score: {score}%</h4>
          <p>
            {score >= 80
              ? 'Great job! You passed the quiz.'
              : 'Keep studying and try again.'}
          </p>
        </div>
      )}

      {quiz.questions.map((question, qIndex) => (
        <div key={question.id} className="quiz-question-container">
          <div className="quiz-question">
            <span className="question-number">{qIndex + 1}.</span> {question.text}
          </div>

          <div className="quiz-options">
            {question.options.map((option, oIndex) => {
              const isSelected = answers[question.id] === oIndex;
              const isCorrect = question.correctAnswer === oIndex;
              const showResult = submitted;

              let optionClass = 'quiz-option';
              if (isSelected) optionClass += ' selected';
              if (showResult && isCorrect) optionClass += ' correct';
              if (showResult && isSelected && !isCorrect) optionClass += ' incorrect';

              return (
                <div
                  key={oIndex}
                  className={optionClass}
                  onClick={() => handleAnswerSelect(question.id, oIndex)}
                >
                  <span className="option-letter">
                    {String.fromCharCode(65 + oIndex)}.
                  </span>
                  {option}
                </div>
              );
            })}
          </div>

          {submitted && question.explanation && (
            <div className="quiz-explanation">
              <strong>Explanation:</strong> {question.explanation}
            </div>
          )}
        </div>
      ))}

      <div className="quiz-actions">
        {!submitted ? (
          <button
            className="quiz-submit-btn"
            onClick={handleSubmit}
            disabled={Object.keys(answers).length < quiz.questions.length}
          >
            Submit Quiz
          </button>
        ) : (
          <button className="quiz-reset-btn" onClick={handleReset}>
            Try Again
          </button>
        )}
      </div>

      <style>{`
        .quiz-container {
          margin: 2rem 0;
          padding: 1.5rem;
          border: 1px solid var(--ifm-color-emphasis-300);
          border-radius: 8px;
          background: var(--ifm-background-surface-color);
        }

        .quiz-container h3 {
          margin-top: 0;
          margin-bottom: 1.5rem;
        }

        .quiz-loading,
        .quiz-error {
          padding: 2rem;
          text-align: center;
          color: var(--ifm-color-emphasis-600);
        }

        .quiz-result {
          padding: 1rem;
          border-radius: 6px;
          margin-bottom: 1.5rem;
          text-align: center;
        }

        .quiz-result h4 {
          margin: 0 0 0.5rem 0;
        }

        .quiz-result p {
          margin: 0;
        }

        .quiz-result-pass {
          background: rgba(46, 133, 85, 0.15);
          border: 1px solid var(--ifm-color-primary);
        }

        .quiz-result-fail {
          background: rgba(220, 53, 69, 0.15);
          border: 1px solid #dc3545;
        }

        .quiz-question-container {
          margin-bottom: 1.5rem;
          padding-bottom: 1.5rem;
          border-bottom: 1px solid var(--ifm-color-emphasis-200);
        }

        .quiz-question-container:last-of-type {
          border-bottom: none;
        }

        .quiz-question {
          font-weight: 600;
          margin-bottom: 1rem;
        }

        .question-number {
          color: var(--ifm-color-primary);
        }

        .quiz-options {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .quiz-option {
          padding: 0.75rem 1rem;
          border: 1px solid var(--ifm-color-emphasis-200);
          border-radius: 4px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .quiz-option:hover:not(.correct):not(.incorrect) {
          background: var(--ifm-color-emphasis-100);
        }

        .quiz-option.selected {
          background: var(--ifm-color-primary-lighter);
          border-color: var(--ifm-color-primary);
        }

        .quiz-option.correct {
          background: rgba(46, 133, 85, 0.2);
          border-color: #2e8555;
        }

        .quiz-option.incorrect {
          background: rgba(220, 53, 69, 0.2);
          border-color: #dc3545;
        }

        .option-letter {
          font-weight: 600;
          margin-right: 0.5rem;
          color: var(--ifm-color-primary);
        }

        .quiz-explanation {
          margin-top: 1rem;
          padding: 0.75rem;
          background: var(--ifm-color-emphasis-100);
          border-radius: 4px;
          font-size: 0.9rem;
        }

        .quiz-actions {
          margin-top: 1.5rem;
          text-align: center;
        }

        .quiz-submit-btn,
        .quiz-reset-btn {
          padding: 0.75rem 2rem;
          border: none;
          border-radius: 6px;
          font-size: 1rem;
          cursor: pointer;
          transition: opacity 0.2s;
        }

        .quiz-submit-btn {
          background: var(--ifm-color-primary);
          color: white;
        }

        .quiz-submit-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .quiz-reset-btn {
          background: var(--ifm-color-emphasis-300);
          color: var(--ifm-font-color-base);
        }

        .quiz-submit-btn:hover:not(:disabled),
        .quiz-reset-btn:hover {
          opacity: 0.9;
        }
      `}</style>
    </div>
  );
};

export default ChapterQuiz;
