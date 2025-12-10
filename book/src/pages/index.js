import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot/Chatbot';
import config from '../utils/config';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Book 📚
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A comprehensive guide to Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--6">
                <h2>🤖 Interactive Learning</h2>
                <p>
                  This book features an integrated RAG (Retrieval-Augmented Generation) chatbot
                  that can answer questions about the book content. Ask questions about specific
                  sections or the entire book for an interactive learning experience.
                </p>

                <h2>📘 Comprehensive Coverage</h2>
                <p>
                  From ROS 2 fundamentals to Vision-Language-Action systems, this book covers
                  all aspects of modern humanoid robotics development with practical examples
                  and hands-on labs.
                </p>

                <h2>🔧 Real-World Applications</h2>
                <p>
                  Learn to build systems that integrate perception, planning, control, and
                  cognitive capabilities for next-generation humanoid robots.
                </p>
              </div>

              <div className="col col--6">
                <div className={styles.chatbotContainer}>
                  <Chatbot backendUrl={config.BACKEND_URL} />
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}