#!/usr/bin/env python3
"""
Query Pattern Analysis Script

This script analyzes user queries and AI responses to identify patterns, gaps, and
opportunities for improvement. It helps make the God Mode system more predictive
by learning from past interactions.

Usage:
    python script_analyze_patterns.py [--days 30]

The script will analyze recent interactions and generate recommendations for
improving the system, enhancing the prompts, and predicting future needs.
"""

import os
import sys
import re
import json
import datetime
import argparse
from pathlib import Path
from collections import Counter, defaultdict
import subprocess

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define key directories
MEMORY_DIR = GOD_MODE_DIR / "memory"
DISCUSSION_DIR = GOD_MODE_DIR / "discussion"
CACHE_DIR = GOD_MODE_DIR / ".cache"
LOGS_DIR = GOD_MODE_DIR / "logs"

# Define output files
PATTERNS_FILE = MEMORY_DIR / "memory_patterns.md"
PROMPT_LEARNINGS_FILE = MEMORY_DIR / "memory_prompt_learnings.md"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    try:
        # Try to use the helper script if available
        timestamp_script = SCRIPT_DIR / "utils" / "script_timestamp.py"
        if timestamp_script.exists():
            result = subprocess.run(
                [sys.executable, str(timestamp_script)],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
    except Exception as e:
        print(f"Error using timestamp script: {e}", file=sys.stderr)
    
    # Fallback to built-in datetime
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def get_recent_discussion_files(days=30):
    """
    Get recent discussion files from the last N days.
    
    Args:
        days (int): Number of days to look back
        
    Returns:
        list: List of discussion file paths
    """
    discussion_files = []
    
    # Calculate the cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    
    # Find all markdown files in the discussion directory
    for root, _, files in os.walk(DISCUSSION_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Check if the file was modified after the cutoff date
                mod_time = os.path.getmtime(file_path)
                mod_date = datetime.datetime.fromtimestamp(mod_time)
                
                if mod_date >= cutoff_date:
                    discussion_files.append(file_path)
    
    return discussion_files

def extract_user_queries(file_path):
    """
    Extract user queries from a discussion file.
    
    Args:
        file_path (str): Path to the discussion file
        
    Returns:
        list: List of user query strings
    """
    queries = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract user queries - this pattern might need to be adjusted
        # based on the actual format of your discussion files
        query_pattern = r'(?:^|\n)## User Query\s*\n(.*?)(?=\n## AI Response|\Z)'
        matches = re.finditer(query_pattern, content, re.DOTALL)
        
        for match in matches:
            query = match.group(1).strip()
            if query:
                queries.append(query)
    
    except Exception as e:
        print(f"Error extracting queries from {file_path}: {e}", file=sys.stderr)
    
    return queries

def extract_ai_responses(file_path):
    """
    Extract AI responses from a discussion file.
    
    Args:
        file_path (str): Path to the discussion file
        
    Returns:
        list: List of AI response strings
    """
    responses = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract AI responses - this pattern might need to be adjusted
        # based on the actual format of your discussion files
        response_pattern = r'(?:^|\n)## AI Response\s*\n(.*?)(?=\n## User Query|\Z)'
        matches = re.finditer(response_pattern, content, re.DOTALL)
        
        for match in matches:
            response = match.group(1).strip()
            if response:
                responses.append(response)
    
    except Exception as e:
        print(f"Error extracting responses from {file_path}: {e}", file=sys.stderr)
    
    return responses

def analyze_query_keywords(queries):
    """
    Analyze keywords used in user queries.
    
    Args:
        queries (list): List of user query strings
        
    Returns:
        Counter: Frequency count of keywords
    """
    # Common English stop words to exclude
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
        'which', 'this', 'that', 'these', 'those', 'then', 'just', 'so', 'than',
        'such', 'both', 'through', 'about', 'for', 'is', 'of', 'while', 'during',
        'to', 'from', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        'can', 'will', 'could', 'should', 'would', 'may', 'might',
        'must', 'need', 'shall', 'want', 'way', 'now', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'done',
        'get', 'got', 'go', 'going', 'went', 'gone',
        'user', 'using', 'use', 'please', 'need', 'make', 'want', 'like',
        'i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours',
        'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
        'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
        'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    }
    
    keywords = Counter()
    
    for query in queries:
        # Tokenize the query into words
        words = re.findall(r'\b\w+\b', query.lower())
        
        # Filter out stop words and short words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Update keyword counts
        keywords.update(filtered_words)
    
    return keywords

def analyze_query_patterns(queries):
    """
    Analyze patterns in user queries.
    
    Args:
        queries (list): List of user query strings
        
    Returns:
        dict: Dictionary of identified patterns
    """
    patterns = {
        'requests': {
            'code_creation': 0,
            'code_modification': 0,
            'documentation': 0,
            'explanation': 0,
            'debugging': 0,
            'optimization': 0,
            'architecture': 0,
            'guidance': 0,
        },
        'topics': {
            'frontend': 0,
            'backend': 0,
            'database': 0,
            'api': 0,
            'security': 0,
            'performance': 0,
            'testing': 0,
            'deployment': 0,
            'ui': 0,
            'ux': 0,
        },
        'directives': {
            'step_by_step': 0,
            'show_example': 0,
            'deep_dive': 0,
            'quick_answer': 0,
            'best_practices': 0,
        },
    }
    
    # Patterns to look for in queries
    request_patterns = {
        'code_creation': [r'create', r'implement', r'build', r'develop', r'code', r'write code for', r'generate'],
        'code_modification': [r'modify', r'update', r'change', r'refactor', r'rewrite', r'fix'],
        'documentation': [r'document', r'explain', r'clarify', r'comment', r'documentation'],
        'explanation': [r'explain', r'describe', r'how does', r'tell me about', r'what is', r'why'],
        'debugging': [r'debug', r'fix', r'error', r'issue', r'bug', r'problem', r'fails', r'doesn\'t work'],
        'optimization': [r'optimize', r'improve', r'speed up', r'performance', r'make .* faster', r'reduce', r'efficient'],
        'architecture': [r'architect', r'design', r'structure', r'system', r'pattern', r'approach', r'strategy'],
        'guidance': [r'guide', r'help', r'advice', r'suggestion', r'recommend', r'best way', r'what should', r'how should'],
    }
    
    topic_patterns = {
        'frontend': [r'frontend', r'ui', r'interface', r'component', r'react', r'vue', r'angular', r'css', r'html'],
        'backend': [r'backend', r'server', r'endpoint', r'middleware', r'express', r'django', r'flask', r'route'],
        'database': [r'database', r'data', r'model', r'schema', r'query', r'sql', r'nosql', r'mongo', r'postgres'],
        'api': [r'api', r'rest', r'graphql', r'endpoint', r'request', r'response', r'http'],
        'security': [r'security', r'authentication', r'authorization', r'auth', r'permission', r'role', r'protect'],
        'performance': [r'performance', r'slow', r'fast', r'speed', r'optimize', r'efficient', r'memory', r'cpu', r'lag'],
        'testing': [r'test', r'unit test', r'integration test', r'e2e', r'testing', r'jest', r'cypress', r'assert'],
        'deployment': [r'deploy', r'deployment', r'ci/cd', r'pipeline', r'production', r'staging', r'release'],
        'ui': [r'ui', r'user interface', r'button', r'form', r'component', r'style', r'css', r'appearance'],
        'ux': [r'ux', r'user experience', r'flow', r'interaction', r'accessibility', r'usability', r'a11y'],
    }
    
    directive_patterns = {
        'step_by_step': [r'step by step', r'steps', r'process', r'procedure', r'how to', r'guide me', r'walk through'],
        'show_example': [r'example', r'sample', r'illustration', r'demonstrate', r'show me', r'code sample'],
        'deep_dive': [r'deep dive', r'in depth', r'detailed', r'thorough', r'comprehensive', r'explain fully'],
        'quick_answer': [r'quick', r'briefly', r'summary', r'tldr', r'short', r'concise', r'simple'],
        'best_practices': [r'best practice', r'recommended', r'standard', r'convention', r'proper way'],
    }
    
    for query in queries:
        query_lower = query.lower()
        
        # Check request patterns
        for category, patterns_list in request_patterns.items():
            for pattern in patterns_list:
                if re.search(r'\b' + pattern + r'\b', query_lower):
                    patterns['requests'][category] += 1
                    break
        
        # Check topic patterns
        for category, patterns_list in topic_patterns.items():
            for pattern in patterns_list:
                if re.search(r'\b' + pattern + r'\b', query_lower):
                    patterns['topics'][category] += 1
                    break
        
        # Check directive patterns
        for category, patterns_list in directive_patterns.items():
            for pattern in patterns_list:
                if re.search(r'\b' + pattern + r'\b', query_lower):
                    patterns['directives'][category] += 1
                    break
    
    return patterns

def analyze_response_effectiveness(queries, responses):
    """
    Analyze the effectiveness of AI responses based on user follow-ups.
    
    Args:
        queries (list): List of user query strings
        responses (list): List of AI response strings
        
    Returns:
        dict: Dictionary of effectiveness metrics
    """
    # Pair queries and responses, assuming they are in order
    interactions = list(zip(queries, responses)) if len(queries) == len(responses) else []
    
    # Metrics to track
    metrics = {
        'follow_up_rate': 0,  # How often users need to ask clarifying questions
        'marker_usage': 0,    # How often responses include proper markers
        'completeness': 0,    # How complete the responses appear to be
        'code_quality': 0,    # How well-formed code in responses appears
    }
    
    # Skip if there are too few interactions
    if len(interactions) < 2:
        return metrics
    
    # Analyze follow-up patterns
    for i in range(len(interactions) - 1):
        query, response = interactions[i]
        next_query = interactions[i + 1][0]
        
        # Check for follow-up questions indicating incomplete responses
        follow_up_indicators = [
            r'(can you )?(explain|clarify) (this|that)',
            r'(what|how) (do|does|about) (the|this|that)',
            r'(i don\'t understand)',
            r'(can you) (be more|provide more) (specific|details)',
            r'(still|also) (have|having) (a|an|some) (question|issue|problem)',
            r'(that\'s not what i|that doesn\'t|this doesn\'t) (meant|mean|asked for|want)',
        ]
        
        for indicator in follow_up_indicators:
            if re.search(indicator, next_query.lower()):
                metrics['follow_up_rate'] += 1
                break
        
        # Check for marker usage
        markers = [
            r'\[LOG_SUMMARY\]',
            r'\[LOG_DETAIL\]',
            r'\[MEMORY_UPDATE\]',
            r'\[FEATURE_LOG',
            r'\[DOC_UPDATE',
        ]
        
        for marker in markers:
            if re.search(marker, response):
                metrics['marker_usage'] += 1
                break
        
        # Check for completeness
        if len(response) > 500:  # Arbitrary threshold for a "complete" response
            metrics['completeness'] += 1
        
        # Check for code quality
        code_blocks = re.findall(r'```(?:[a-z]*\n)?(.*?)```', response, re.DOTALL)
        if code_blocks:
            # Basic check - does the code have proper indentation and no obvious errors?
            for code in code_blocks:
                if re.search(r'^\s+', code, re.MULTILINE) and not re.search(r'error|exception|undefined|null', code.lower()):
                    metrics['code_quality'] += 1
    
    # Normalize metrics
    total = len(interactions) - 1
    if total > 0:
        metrics['follow_up_rate'] = metrics['follow_up_rate'] / total
        metrics['marker_usage'] = metrics['marker_usage'] / total
        metrics['completeness'] = metrics['completeness'] / total
        metrics['code_quality'] = metrics['code_quality'] / (total if len(code_blocks) > 0 else 1)
    
    return metrics

def identify_improvement_opportunities(keywords, patterns, effectiveness):
    """
    Identify opportunities for improving the God Mode system.
    
    Args:
        keywords (Counter): Frequency count of keywords
        patterns (dict): Dictionary of identified patterns
        effectiveness (dict): Dictionary of effectiveness metrics
        
    Returns:
        list: List of improvement opportunities
    """
    opportunities = []
    
    # Check for high-frequency topics that might need specialized notepads
    common_topics = [topic for topic, count in patterns['topics'].items() if count > 0]
    for topic in common_topics:
        opportunities.append({
            'type': 'notepad',
            'topic': topic,
            'description': f"Consider creating a specialized notepad for '{topic}' topics."
        })
    
    # Check for high follow-up rate indicating incomplete responses
    if effectiveness['follow_up_rate'] > 0.3:  # If > 30% of responses get follow-ups
        opportunities.append({
            'type': 'prompt',
            'description': "Consider enhancing prompts to encourage more complete responses."
        })
    
    # Check for low marker usage
    if effectiveness['marker_usage'] < 0.7:  # If < 70% of responses use markers
        opportunities.append({
            'type': 'rules',
            'description': "Strengthen rules to ensure consistent use of markers in responses."
        })
    
    # Check for common request types that might need specialized handling
    common_requests = [req for req, count in patterns['requests'].items() if count > 0]
    for request in common_requests:
        opportunities.append({
            'type': 'workflow',
            'request': request,
            'description': f"Consider optimizing workflow for '{request}' requests."
        })
    
    return opportunities

def generate_improvement_recommendations(keywords, patterns, effectiveness, opportunities):
    """
    Generate specific recommendations for improving the God Mode system.
    
    Args:
        keywords (Counter): Frequency count of keywords
        patterns (dict): Dictionary of identified patterns
        effectiveness (dict): Dictionary of effectiveness metrics
        opportunities (list): List of improvement opportunities
        
    Returns:
        str: Markdown formatted recommendations
    """
    timestamp = get_timestamp()
    
    # Start with title and overview
    markdown = [
        f"# God Mode Improvement Recommendations\n\n",
        f"*Generated: {timestamp}*\n\n",
        "## Overview\n\n",
        "Based on analysis of recent user queries and AI responses, this document provides recommendations for enhancing the God Mode system's predictive capabilities.\n\n",
    ]
    
    # Add usage pattern summary
    markdown.append("## Usage Pattern Summary\n\n")
    
    # Add top keywords
    top_keywords = keywords.most_common(10)
    if top_keywords:
        markdown.append("### Top Keywords\n\n")
        for keyword, count in top_keywords:
            markdown.append(f"- **{keyword}**: {count} occurrences\n")
        markdown.append("\n")
    
    # Add request patterns
    markdown.append("### Request Types\n\n")
    for request, count in sorted(patterns['requests'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            markdown.append(f"- **{request}**: {count} occurrences\n")
    markdown.append("\n")
    
    # Add topic patterns
    markdown.append("### Topic Areas\n\n")
    for topic, count in sorted(patterns['topics'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            markdown.append(f"- **{topic}**: {count} occurrences\n")
    markdown.append("\n")
    
    # Add directive patterns
    markdown.append("### Directive Types\n\n")
    for directive, count in sorted(patterns['directives'].items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            markdown.append(f"- **{directive}**: {count} occurrences\n")
    markdown.append("\n")
    
    # Add effectiveness metrics
    markdown.append("## Response Effectiveness\n\n")
    markdown.append(f"- **Follow-up Rate**: {effectiveness['follow_up_rate']:.2f} (lower is better)\n")
    markdown.append(f"- **Marker Usage**: {effectiveness['marker_usage']:.2f} (higher is better)\n")
    markdown.append(f"- **Completeness**: {effectiveness['completeness']:.2f} (higher is better)\n")
    markdown.append(f"- **Code Quality**: {effectiveness['code_quality']:.2f} (higher is better)\n\n")
    
    # Add improvement recommendations
    markdown.append("## Improvement Recommendations\n\n")
    
    # Group opportunities by type
    opportunities_by_type = defaultdict(list)
    for opportunity in opportunities:
        opportunities_by_type[opportunity['type']].append(opportunity)
    
    # Add recommendations by type
    for type_name, type_opportunities in opportunities_by_type.items():
        markdown.append(f"### {type_name.title()} Improvements\n\n")
        for i, opportunity in enumerate(type_opportunities, 1):
            markdown.append(f"{i}. {opportunity['description']}\n")
        markdown.append("\n")
    
    # Add specific suggestions for top keywords
    markdown.append("## Predictive Enhancement Suggestions\n\n")
    
    # Suggest notepads based on top keywords
    suggested_notepads = set()
    for keyword, _ in top_keywords[:5]:
        notepad_name = f"notepad_{keyword.lower()}"
        suggested_notepads.add(notepad_name)
    
    if suggested_notepads:
        markdown.append("### Suggested Specialized Notepads\n\n")
        for notepad in sorted(suggested_notepads):
            markdown.append(f"- `{notepad}.md`: Focused on {notepad.replace('notepad_', '')} topics\n")
        markdown.append("\n")
    
    # Suggest prompt enhancements based on patterns
    markdown.append("### Prompt Enhancement Guidelines\n\n")
    
    # Common request types
    top_requests = [req for req, count in sorted(patterns['requests'].items(), key=lambda x: x[1], reverse=True)[:3] if count > 0]
    if top_requests:
        markdown.append("When the AI detects these request types, it should:\n\n")
        for request in top_requests:
            if request == 'code_creation':
                markdown.append("- For **code creation**: Include comprehensive comments, error handling, and tests\n")
            elif request == 'code_modification':
                markdown.append("- For **code modification**: Always show before/after comparisons and explain the changes\n")
            elif request == 'documentation':
                markdown.append("- For **documentation**: Structure with clear sections and include examples\n")
            elif request == 'explanation':
                markdown.append("- For **explanation**: Use analogies and visual descriptions when helpful\n")
            elif request == 'debugging':
                markdown.append("- For **debugging**: Suggest multiple possible causes and verification steps\n")
            elif request == 'optimization':
                markdown.append("- For **optimization**: Explain performance impacts and tradeoffs\n")
            elif request == 'architecture':
                markdown.append("- For **architecture**: Include diagrams and consider alternative approaches\n")
            elif request == 'guidance':
                markdown.append("- For **guidance**: Provide options with pros and cons\n")
        markdown.append("\n")
    
    # Common topics
    top_topics = [topic for topic, count in sorted(patterns['topics'].items(), key=lambda x: x[1], reverse=True)[:3] if count > 0]
    if top_topics:
        markdown.append("The AI should proactively reference these resources for common topics:\n\n")
        for topic in top_topics:
            if topic == 'frontend':
                markdown.append("- For **frontend**: Reference UI guidelines and component patterns\n")
            elif topic == 'backend':
                markdown.append("- For **backend**: Reference API patterns and server architecture\n")
            elif topic == 'database':
                markdown.append("- For **database**: Reference data models and query patterns\n")
            elif topic == 'api':
                markdown.append("- For **api**: Reference API documentation and REST/GraphQL patterns\n")
            elif topic == 'security':
                markdown.append("- For **security**: Reference security guidelines and authentication flows\n")
            elif topic == 'performance':
                markdown.append("- For **performance**: Reference performance metrics and optimization techniques\n")
            elif topic == 'testing':
                markdown.append("- For **testing**: Reference testing strategies and test patterns\n")
            elif topic == 'deployment':
                markdown.append("- For **deployment**: Reference deployment workflows and CI/CD pipelines\n")
            elif topic == 'ui':
                markdown.append("- For **ui**: Reference UI guidelines and design patterns\n")
            elif topic == 'ux':
                markdown.append("- For **ux**: Reference UX principles and user workflows\n")
        markdown.append("\n")
    
    # Add conclusion
    markdown.append("## Conclusion\n\n")
    markdown.append("By implementing these recommendations, the God Mode system can become more predictive and provide higher quality assistance. Regular analysis of user interactions will help identify new patterns and further improve the system.\n\n")
    markdown.append("*This report was automatically generated based on interaction analysis. Please review and implement recommendations as appropriate.*\n")
    
    return ''.join(markdown)

def generate_prompt_learnings(keywords, patterns, effectiveness, opportunities):
    """
    Generate learnings for improving prompts based on interaction analysis.
    
    Args:
        keywords (Counter): Frequency count of keywords
        patterns (dict): Dictionary of identified patterns
        effectiveness (dict): Dictionary of effectiveness metrics
        opportunities (list): List of improvement opportunities
        
    Returns:
        str: Markdown formatted prompt learnings
    """
    timestamp = get_timestamp()
    
    # Start with title and introduction
    markdown = [
        f"## {timestamp}\n\n",
        "### Prompt Improvement Insights\n\n",
    ]
    
    # Add insights based on effectiveness metrics
    if effectiveness['follow_up_rate'] > 0.3:
        markdown.append("#### Completeness Improvement\n\n")
        markdown.append("The AI should focus on more complete responses to reduce follow-up questions. Specific strategies:\n\n")
        markdown.append("- Anticipate related questions and address them proactively\n")
        markdown.append("- Ensure all parts of multi-part questions are answered\n")
        markdown.append("- Provide context and explanations along with code examples\n")
        markdown.append("- Consider both immediate and long-term implications of solutions\n\n")
    
    if effectiveness['marker_usage'] < 0.7:
        markdown.append("#### Marker Usage Improvement\n\n")
        markdown.append("The AI should consistently use appropriate markers to enable automatic documentation. Strategies:\n\n")
        markdown.append("- Always include [LOG_SUMMARY] and [LOG_DETAIL] for significant changes\n")
        markdown.append("- Use [MEMORY_UPDATE] for important context that should be remembered\n")
        markdown.append("- Use specialized memory markers for specific knowledge areas\n")
        markdown.append("- Use [FEATURE_LOG] for feature-specific implementation details\n")
        markdown.append("- Use [DOC_UPDATE] for updates to official documentation\n\n")
    
    # Add insights based on top request types
    top_requests = [req for req, count in sorted(patterns['requests'].items(), key=lambda x: x[1], reverse=True)[:3] if count > 0]
    if top_requests:
        markdown.append("#### Common Request Type Optimization\n\n")
        markdown.append("The AI should optimize responses for these common request types:\n\n")
        for request in top_requests:
            if request == 'code_creation':
                markdown.append("- **Code Creation**: Include structure overview before code, add detailed comments\n")
            elif request == 'code_modification':
                markdown.append("- **Code Modification**: Show before/after diff, explain reasoning for changes\n")
            elif request == 'documentation':
                markdown.append("- **Documentation**: Use standardized formats, include examples\n")
            elif request == 'explanation':
                markdown.append("- **Explanation**: Start with high-level summary, then add details\n")
            elif request == 'debugging':
                markdown.append("- **Debugging**: Analyze possible causes systematically\n")
            elif request == 'optimization':
                markdown.append("- **Optimization**: Provide metrics and multiple approaches\n")
            elif request == 'architecture':
                markdown.append("- **Architecture**: Include diagrams, explain trade-offs\n")
            elif request == 'guidance':
                markdown.append("- **Guidance**: List options with pros/cons, make recommendations\n")
    
    # Add predictive suggestions based on patterns
    markdown.append("#### Predictive Enhancement Opportunities\n\n")
    markdown.append("Based on usage patterns, the AI should proactively:\n\n")
    
    # Add suggestions based on top topics
    top_topics = [topic for topic, count in sorted(patterns['topics'].items(), key=lambda x: x[1], reverse=True)[:3] if count > 0]
    for topic in top_topics:
        if topic == 'frontend':
            markdown.append("- Reference UI components and design patterns for frontend questions\n")
        elif topic == 'backend':
            markdown.append("- Include architecture considerations for backend questions\n")
        elif topic == 'database':
            markdown.append("- Discuss data integrity and performance for database questions\n")
        elif topic == 'api':
            markdown.append("- Reference RESTful best practices for API questions\n")
        elif topic == 'security':
            markdown.append("- Include security implications in all code examples\n")
        elif topic == 'performance':
            markdown.append("- Discuss optimization strategies for performance questions\n")
        elif topic == 'testing':
            markdown.append("- Include test examples for implementation questions\n")
        elif topic == 'deployment':
            markdown.append("- Consider deployment contexts for configuration questions\n")
    
    # Add closing recommendations
    markdown.append("\nThese patterns should be incorporated into the enhanced_prompt.md file to improve AI responses without requiring explicit user instructions.\n")
    
    return ''.join(markdown)

def update_patterns_file(content):
    """
    Update the patterns file with new content.
    
    Args:
        content (str): New content to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_directory_exists(os.path.dirname(PATTERNS_FILE))
        
        # Check if file exists
        if PATTERNS_FILE.exists():
            # Read existing content
            with open(PATTERNS_FILE, 'r') as f:
                existing_content = f.read()
            
            # Don't overwrite the title and introduction
            title_pattern = r'^# God Mode Improvement Recommendations\s+\*Generated:[^*]*\*\s+## Overview[^\n]*\n\n'
            match = re.search(title_pattern, existing_content, re.MULTILINE | re.DOTALL)
            if match:
                # Keep the title and introduction, replace the rest
                title_intro = match.group(0)
                rest_of_content = content[content.find('## Usage Pattern Summary'):]
                new_content = title_intro + rest_of_content
            else:
                new_content = content
        else:
            new_content = content
        
        # Write the updated content
        with open(PATTERNS_FILE, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated {PATTERNS_FILE}")
        return True
    
    except Exception as e:
        print(f"Error updating patterns file: {e}", file=sys.stderr)
        return False

def update_prompt_learnings_file(content):
    """
    Update the prompt learnings file with new content.
    
    Args:
        content (str): New content to append
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        ensure_directory_exists(os.path.dirname(PROMPT_LEARNINGS_FILE))
        
        # Check if file exists
        if PROMPT_LEARNINGS_FILE.exists():
            # Read existing content
            with open(PROMPT_LEARNINGS_FILE, 'r') as f:
                existing_content = f.read()
            
            # Append new content
            new_content = existing_content + "\n\n" + content
        else:
            # Create new file with header and content
            new_content = "# Prompt Learning Insights\n\n" + \
                         "This document captures insights for improving AI prompts based on analysis of user interactions.\n\n" + \
                         content
        
        # Write the updated content
        with open(PROMPT_LEARNINGS_FILE, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated {PROMPT_LEARNINGS_FILE}")
        return True
    
    except Exception as e:
        print(f"Error updating prompt learnings file: {e}", file=sys.stderr)
        return False

def main():
    """Main function to parse arguments and analyze patterns."""
    parser = argparse.ArgumentParser(
        description='Analyze user query patterns and suggest system improvements'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to look back for discussions (default: 30)'
    )
    args = parser.parse_args()
    
    print(f"Analyzing user queries from the past {args.days} days...")
    
    # Get recent discussion files
    discussion_files = get_recent_discussion_files(args.days)
    print(f"Found {len(discussion_files)} discussion files")
    
    # Skip if no files found
    if not discussion_files:
        print("No recent discussion files found. Nothing to analyze.")
        return 0
    
    # Extract queries and responses
    all_queries = []
    all_responses = []
    
    for file_path in discussion_files:
        queries = extract_user_queries(file_path)
        responses = extract_ai_responses(file_path)
        all_queries.extend(queries)
        all_responses.extend(responses)
    
    print(f"Extracted {len(all_queries)} user queries and {len(all_responses)} AI responses")
    
    # Skip if too few queries
    if len(all_queries) < 5:
        print("Not enough queries to analyze. Need at least 5 queries.")
        return 0
    
    # Analyze queries
    keywords = analyze_query_keywords(all_queries)
    patterns = analyze_query_patterns(all_queries)
    effectiveness = analyze_response_effectiveness(all_queries, all_responses)
    
    # Identify improvement opportunities
    opportunities = identify_improvement_opportunities(keywords, patterns, effectiveness)
    
    # Generate recommendations
    recommendations = generate_improvement_recommendations(
        keywords, patterns, effectiveness, opportunities
    )
    
    # Generate prompt learnings
    prompt_learnings = generate_prompt_learnings(
        keywords, patterns, effectiveness, opportunities
    )
    
    # Update files
    update_patterns_file(recommendations)
    update_prompt_learnings_file(prompt_learnings)
    
    print("Pattern analysis complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 