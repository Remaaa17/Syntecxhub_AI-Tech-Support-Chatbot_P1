"""
Export Manager - Export conversations to PDF and JSON
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class ExportManager:
    """Handles exporting conversations to various formats"""
    
    def __init__(self, context_manager):
        """
        Initialize export manager
        
        Args:
            context_manager: Reference to context manager
        """
        self.context_manager = context_manager
        
    def export_to_json(self, user_id: str, filepath: str) -> bool:
        """
        Export conversation to JSON
        
        Args:
            user_id: User identifier
            filepath: Output file path
            
        Returns:
            True if successful
        """
        try:
            context = self.context_manager.get_context(user_id)
            metadata = self.context_manager.get_user_metadata(user_id)
            
            export_data = {
                'user_id': user_id,
                'exported_at': datetime.now().isoformat(),
                'metadata': metadata,
                'messages': context
            }
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] JSON export failed: {e}")
            return False
    
    def export_to_text(self, user_id: str, filepath: str) -> bool:
        """
        Export conversation to plain text
        
        Args:
            user_id: User identifier
            filepath: Output file path
            
        Returns:
            True if successful
        """
        try:
            context = self.context_manager.get_context(user_id)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("Tech Support Chat History\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"User ID: {user_id}\n")
                f.write("=" * 60 + "\n\n")
                
                for msg in context:
                    sender = "You" if msg['sender'] == 'user' else "Tech Support"
                    timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
                    f.write(f"[{timestamp}] {sender}:\n")
                    f.write(f"{msg['message']}\n\n")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Text export failed: {e}")
            return False
    
    def export_to_pdf(self, user_id: str, filepath: str) -> bool:
        """
        Export conversation to PDF
        
        Args:
            user_id: User identifier  
            filepath: Output file path
            
        Returns:
            True if successful
        """
        try:
            # Try using fpdf
            from fpdf import FPDF
            
            context = self.context_manager.get_context(user_id)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            
            # Title
            pdf.cell(0, 10, "Tech Support Chat History", ln=True, align='C')
            pdf.set_font("Arial", "", 10)
            pdf.cell(0, 10, f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
            pdf.cell(0, 10, f"User ID: {user_id}", ln=True, align='C')
            pdf.ln(10)
            
            # Messages
            pdf.set_font("Arial", "", 11)
            
            for msg in context:
                sender = "You" if msg['sender'] == 'user' else "Tech Support"
                timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
                
                # Sender and time
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, f"[{timestamp}] {sender}:", ln=True)
                
                # Message
                pdf.set_font("Arial", "", 10)
                # Handle multi-line messages
                message_lines = msg['message'].split('\n')
                for line in message_lines:
                    pdf.multi_cell(0, 6, line)
                
                pdf.ln(3)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            pdf.output(filepath)
            
            return True
            
        except ImportError:
            print("[ERROR] fpdf not installed. Install with: pip install fpdf")
            return False
        except Exception as e:
            print(f"[ERROR] PDF export failed: {e}")
            return False
    
    def export_conversation(self, user_id: str, format: str = 'json', 
                          output_dir: str = 'exports') -> str:
        """
        Export conversation in specified format
        
        Args:
            user_id: User identifier
            format: Export format ('json', 'text', 'pdf')
            output_dir: Output directory
            
        Returns:
            Path to exported file or empty string on failure
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"chat_{user_id}_{timestamp}"
        
        if format == 'json':
            filepath = os.path.join(output_dir, f"{filename}.json")
            success = self.export_to_json(user_id, filepath)
        elif format == 'text':
            filepath = os.path.join(output_dir, f"{filename}.txt")
            success = self.export_to_text(user_id, filepath)
        elif format == 'pdf':
            filepath = os.path.join(output_dir, f"{filename}.pdf")
            success = self.export_to_pdf(user_id, filepath)
        else:
            print(f"[ERROR] Unknown format: {format}")
            return ""
        
        if success:
            print(f"[OK] Conversation exported to: {filepath}")
            return filepath
        else:
            return ""
