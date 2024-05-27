import React from 'react';

const Article = ({ article }) => {
    return (
        <div className="article-container">
            <h1>{article.title}</h1>
            <p><strong>By:</strong> {article.author_id}</p>
            <p><strong>Published on:</strong> {new Date(article.published_date.seconds * 1000).toLocaleDateString()}</p>
            <p>{article.summary}</p>
            <img src={article.image_url} alt={article.title} />
            
            {article.content.map((block, index) => {
                switch (block.type) {
                    case 'paragraph':
                        return <p key={index}>{block.content}</p>;
                    case 'heading':
                        return React.createElement(`h${block.level}`, { key: index }, block.content);
                    case 'list':
                        return (
                            <ul key={index}>
                                {block.items.map((item, idx) => <li key={idx}>{item}</li>)}
                            </ul>
                        );
                    default:
                        return null;
                }
            })}
            
            {article.video_url && (
                <div>
                    <video controls>
                        <source src={article.video_url} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            )}

            <div>
                <strong>Tags:</strong>
                <ul>
                    {article.tags.map((tag, index) => (
                        <li key={index}>{tag}</li>
                    ))}
                </ul>
            </div>
            <div>
                <strong>Category:</strong> {article.category}
            </div>
            <div>
                <strong>Attachments:</strong>
                <ul>
                    {article.attachments.map((attachment, index) => (
                        <li key={index}><a href={attachment}>Attachment {index + 1}</a></li>
                    ))}
                </ul>
            </div>
            <div>
                <strong>Comments:</strong>
                <ul>
                    {article.comments.map((comment, index) => (
                        <li key={index}>{comment}</li>
                    ))}
                </ul>
            </div>
            <div>
                <strong>Views:</strong> {article.views}
                <strong> Likes:</strong> {article.likes}
                <strong> Shares:</strong> {article.shares}
            </div>
        </div>
    );
}

// export default Article;
import axios from 'axios';

// Function to send a message to a channel
const sendMessage = async (channelId, content, senderId) => {
    try {
        const response = await axios.post(`/api/channels/${channelId}/messages/send/`, { content, sender_id: senderId });
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error.response.data);
        throw error;
    }
};

// Function to get messages from a channel
const getChannelMessages = async (channelId) => {
    try {
        const response = await axios.get(`/api/channels/${channelId}/messages/`);
        return response.data;
    } catch (error) {
        console.error('Error getting channel messages:', error.response.data);
        throw error;
    }
};

export { sendMessage, getChannelMessages };
import { useEffect, useState } from 'react';
import { sendMessage, getChannelMessages } from '../api/messages'; // Adjust the path as necessary

function ChannelChat({ channelId }) {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const messages = await getChannelMessages(channelId);
                setMessages(messages);
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };

        fetchMessages();
    }, [channelId]);

    const handleSendMessage = async () => {
        try {
            await sendMessage(channelId, newMessage, 'current_user_id'); // Replace 'current_user_id' with the actual sender's ID
            setNewMessage('');
            // Optionally, you can fetch the messages again after sending a new message
            // await fetchMessages();
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div>
            {/* Display messages */}
            {messages.map((message, index) => (
                <div key={index}>
                    <p>{message.content}</p>
                    <p>Sent by: {message.sender_id}</p>
                    <p>Sent at: {message.sent_at}</p>
                </div>
            ))}
            
            {/* Input form to send new message */}
            <div>
                <input type="text" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} />
                <button onClick={handleSendMessage}>Send Message</button>
            </div>
        </div>
    );
}

export default ChannelChat;
