import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';

export default function ChatbotPage(): JSX.Element {
  return (
    <Layout
      title="Chatbot"
      description="Chat with the book content using AI">
      <main>
        <Chatbot />
      </main>
    </Layout>
  );
}