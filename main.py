try:
    import os
    import sys
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.prompt import Prompt
    from agent import ExamPrepAgent
except ImportError as e:
    print(f"Error: Missing dependencies. {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

console = Console()

def main():
    console.print(Panel.fit("[bold blue]ExamPrep Agent[/bold blue]\n[green]Your AI Revision Partner[/green]"))

    # Check for API Key
    if not os.getenv("GEMINI_API_KEY"):
         console.print("[bold red]Warning:[/bold red] GEMINI_API_KEY not found in environment variables.")
         key = Prompt.ask("Please enter your Gemini API Key")
         if key:
             os.environ["GEMINI_API_KEY"] = key

    # Input Phase
    topic = Prompt.ask("[bold yellow]Enter Topic[/bold yellow]")
    exam_type = Prompt.ask("[bold yellow]Exam Type[/bold yellow]", choices=["school", "university", "interview", "competitive"], default="university")
    difficulty = Prompt.ask("[bold yellow]Difficulty[/bold yellow]", choices=["beginner", "intermediate", "advanced"], default="intermediate")

    agent = ExamPrepAgent()
    
    with console.status("[bold green]Planning session...[/bold green]"):
        try:
            plan = agent.start_session(topic, exam_type, difficulty)
            console.print(Markdown(plan))
        except Exception as e:
            console.print(f"[bold red]Error starting session:[/bold red] {e}")
            return

    # Main Loop
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[green]Good luck with your exams! Goodbye![/green]")
                break
            
            if not user_input.strip():
                continue

            with console.status("[bold green]Thinking...[/bold green]"):
                response = agent.handle_input(user_input)
                console.print(Markdown(response))
                
        except KeyboardInterrupt:
            console.print("\n[green]Session interrupted. Goodbye![/green]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
