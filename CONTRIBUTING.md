# Contributing to KUKA_KVP_Command_Interface

Thank you for your interest in contributing! Here's how to get started, how we manage branches, and how to make useful, reviewable contributions.

## 🧭 Branching & Workflow Overview

We maintain **five long-lived branches** in this repository:

- `humble` — main stable branch for ROS 2 Humble.  
- `humble-develop` — active development for Humble. Contributors should *fork from* or *PR into* this branch.  
- `jazzy` — future stable branch (next default ROS 2 version).  
- `jazzy-develop` — active development for Jazzy.  
- `ros1-noetic` — legacy branch for ROS 1 Noetic; deprecated for new features but maintained for backward compatibility.

### Why this structure

- We separate **development** (`*-develop`) from **release/stable** (`humble` / `jazzy`).  
- Contributors work primarily in `humble-develop` (or `jazzy-develop` if targeting that version).  
- Once we're ready, we periodically merge from `humble-develop` → `humble` to create a stable release.  
- The `ros1-noetic` branch stays around only for maintenance; contributions there should be rare and clearly justified.

## How to Contribute

1. **Fork** the repository to your GitHub account.  
2. Clone your fork:

```bash
   git clone git@github.com:your-username/kuka_kvp_command_interface.git
   cd kuka_kvp_command_interface
```

3.  **Create a branch** for your work.
    
    -   If you're working on a feature / bug for **Humble**, branch off `humble-develop`:
        
        ```bash
        git fetch upstream
        git checkout -b feature/my-feature upstream/humble-develop
        
        ```
        
    -   Similarly, for **Jazzy**, branch from `jazzy-develop`:
        
        ```bash
        git checkout -b feature/jazzy-new upstream/jazzy-develop
        
        ```
        
    -   For _rare_ maintenance on Noetic, branch from `ros1-noetic`.
        
4.  **Make your changes**, commit logically, and push to your fork:
    
    ```bash
    git push -u origin feature/my-feature
    
    ```
    
5.  **Open a Pull Request** (PR) against the appropriate target branch in the upstream repository (humble-develop or jazzy-develop):
    
    -   Choose a descriptive title.
        
    -   Explain _what_ you changed, _why_, and any impact.
        
    -   Reference any related issue (e.g., `Closes #123`).
        
    -   If your PR fixes a bug in the stable branch, mention whether this needs cherry-picking to `humble` (or `jazzy`) by maintainers.
        
6.  **Respond to review feedback.** We may ask for changes, clarifications, or updates. We're happy to help you improve your PR.
    
7.  **Merge to stable branch:**
    
    -   The maintainers will periodically merge from the `*-develop` to the stable branch (`humble` or `jazzy`) when ready for a release.
        
    -   We may squash commits, rebase, or cherry-pick as needed for clarity and stability.
        


## Issue Reporting & Feature Requests

-   Use **GitHub Issues** for bug reports or feature ideas.
    
-   When opening an issue, provide:
    
    -   A clear, descriptive title
        
    -   Steps to reproduce (if relevant)
        
    -   Your environment (OS, ROS version, configs)
        
    -   Expected vs actual behavior
        
    -   Logs, stack traces, or error messages if available
        
-   For feature requests, consider also suggesting an implementation or design approach.
    

## Communication & Review

-   Be respectful, inclusive, and constructive in discussions.
    
-   Use the **Discussions** tab for brainstorming or design-level conversations.
    
-   If you're a new contributor, ask maintainers for “good first issue” suggestions.
    

## Deprecated / Legacy Compatibility (`ros1-noetic`)

-   We _do not encourage_ new feature development on the `ros1-noetic` branch — it's primarily for bug fixes or legacy support.
    
-   If you're making a fix here, please:
    
    1.  Open a PR against `ros1-noetic`.
        
    2.  Clearly explain why the change is needed and whether it should be backported to `humble` (or forward-ported to `humble-develop`).
        
    3.  Maintainers may cherry-pick or rebase as appropriate.
        

## License

By contributing, you agree that your contributions will be under the same license as the project. Please ensure you have read and understood the LICENSE file.

----------
