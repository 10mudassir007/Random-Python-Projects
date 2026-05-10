import { useState, type KeyboardEvent } from 'react'
import Sidebar from './components/Sidebar'
import OutputBox from './components/OutputBox'
import './App.css'

export interface Config {
  apiBase: string
  token: string
}

interface ReadmeResponse {
  readme: string
}

interface ValidationError {
  loc: (string | number)[]
  msg: string
  type: string
}

interface ErrorResponse {
  detail?: ValidationError[] | string
}

function App() {
  const [config, setConfig] = useState<Config>({
    apiBase: import.meta.env.VITE_API_BASE_URL ?? '',
    token: '',
  })
  const [repoUrl, setRepoUrl] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generate = async () => {
    const url = repoUrl.trim()
    if (!url) {
      setError('enter a github repo url')
      return
    }

    setError('')
    setOutput('')
    setLoading(true)

    try {
      const base = config.apiBase.trim().replace(/\/$/, '')
      const fullUrl = `${base}/generate`
    # NLP-Projects

Welcome to the **NLP-Projects** repository! This collection features a variety of Natural Language Processing projects, ranging from basic text classification and sentiment analysis to advanced transformer fine-tuning and generative modeling.

---

## 📁 Repository Structure

*   **[Bert Fine-Tuning/](Bert-Fine-Tuning/)**: Implementation of BERT models for SMS spam classification.
*   **[Emotion-Recognition-from-Text/](Emotion-Recognition-from-Text/)**: Deep learning (LSTM) and traditional machine learning (Naive Bayes) approaches to detect emotions in text. Includes a FastAPI web interface.
*   **[Fake-News-Detection/](Fake-News-Detection/)**: Comparative study of various classifiers (Logistic Regression, Decision Trees, Random Forest) for detecting fake news.
*   **[GPT-FINETUNING/](GPT-FINETUNING/)**: Fine-tuning GPT-2 for specialized text generation tasks using the Hugging Face ecosystem.
*   **[Neural-Based-Reasoning/](Neural-Based-Reasoning/)**: A neural network model utilizing Universal Sentence Encoders for boolean question answering.
*   **[Text Generation with LSTM/](Text-Generation-with-LSTM/)**: A character-level LSTM model trained to generate poetry.
*   **[Topic Modelling/](Topic-Modelling/)**: Comparison of classical LDA (Latent Dirichlet Allocation) versus modern BERTopic modeling.

---

## 🚀 Key Technologies & Frameworks
- **Deep Learning**: PyTorch, TensorFlow/Keras
- **NLP Libraries**: Hugging Face Transformers, NLTK, spaCy, Gensim, BERTopic
- **Machine Learning**: Scikit-learn
- **API Development**: FastAPI

---

## 🛠 Project Highlights

### 1. Transformer Fine-Tuning
- **BERT**: Fine-tuned `bert-base-uncased` for sequence classification tasks.
- **GPT-2**: Fine-tuned causal language models to generate technical responses based on software engineering datasets.

### 2. Emotion Recognition
- Provides a dual approach:
    - **LSTM**: Capturing sequential dependencies for high-accuracy emotion detection.
    - **Naive Bayes (TF-IDF)**: A lightweight, performant baseline.
- **Deployment**: Includes a `FastAPI` service with a `Jinja2` template for real-time inference.

### 3. Topic Modeling
- Demonstrates how to extract insights from large text corpora using:
    - **LDA**: Traditional probabilistic topic modeling.
    - **BERTopic**: Leveraging transformer embeddings for cluster-based topic extraction.

---

## 📊 Evaluation
Most projects include Jupyter Notebooks (`.ipynb`) containing end-to-end pipelines:
1.  **Data Ingestion**: Loading datasets from Kaggle/TensorFlow Hub.
2.  **Preprocessing**: Text cleaning, tokenization, and vectorization.
3.  **Training**: Model definition, hyperparameter tuning, and training loops.
4.  **Evaluation**: Visualizations (Confusion Matrices, Loss/Accuracy curves) and model saving for production.

---

## 📝 License
This repository is open-source and available for educational purposes. Feel free to explore, clone, and experiment with the code!

*Developed by [10mudassir007](https://github.com/10mudassir007)*
    // DEBUG: Log the actual URL being called
      console.log('Calling API:', fullUrl)
      console.log('API Base from env:', import.meta.env.VITE_API_BASE_URL)
      console.log('Config apiBase:', config.apiBase)
      const body: { url: string; token?: string } = { url }
      if (config.token.trim()) body.token = config.token.trim()

      const res = await fetch(fullUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      if (!res.ok) {
        const err: ErrorResponse = await res.json().catch(() => ({}))
        const msg = Array.isArray(err.detail)
          ? err.detail[0]?.msg
          : (err.detail ?? `error ${res.status}`)
        throw new Error(msg as string)
      }

      const data: ReadmeResponse = await res.json()
      setOutput(data.readme ?? '')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') generate()
  }

  return (
    <div className="app">
      <Sidebar config={config} onConfigChange={setConfig} />
      <main className="main">
        <header className="main-header">
          <h1 className="main-title">Generate README</h1>
          <p className="main-sub">paste a public github repo url</p>
        </header>

        <div className="url-row">
          <input
            className="url-input"
            type="text"
            placeholder="https://github.com/user/repo"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            onKeyDown={handleKey}
            aria-label="Repository URL"
          />
          <button className="gen-btn" onClick={generate} disabled={loading}>
            {loading ? <span className="spinner" /> : <span className="spark">✦</span>}
            {loading ? 'generating...' : 'Generate'}
          </button>
        </div>

        {error && <div className="error-msg" role="alert">{error}</div>}

        <OutputBox
          output={output}
          onClear={() => { setOutput(''); setRepoUrl('') }}
        />
      </main>
    </div>
  )
}

export default App