
import requests
import json
import csv
import argparse
import sys
import os
import re
from urllib.parse import quote_plus
from datetime import datetime
import time
from fpdf import FPDF
from collections import Counter

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clean_text(text):
    """Remove caracteres que o FPDF (latin-1) não consegue processar"""
    if not text:
        return ""
    return text.encode('ascii', 'ignore').decode('ascii')

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(63, 81, 181)
        self.cell(0, 15, 'RELATÓRIO DE INVESTIGAÇÃO KGB_ARRUDA INSTAOSINT', 0, 1, 'C')
        self.set_draw_color(63, 81, 181)
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()} | Informações sensíveis obtidas via API do Instagram (osint) | Gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, clean_text(title), 0, 1, 'L', True)
        self.ln(4)

class InstagramInvestigatorV2:
    def __init__(self):
        self.current_data = {}
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "x-ig-app-id": "936619743392459"
        }

    def print_banner(self):
        banner = f"""
{Colors.HEADER}{Colors.BOLD}
║ 💀💀💀💀Instagram Scrapper KGB_Arruda 💀💀💀💀 ║
║                                                ║
║                                                ║
║  👮👮👮👮👮👮Para fins investigativos.         ║
║                                                ║
║  arrudacibersec@proton.me  🖥️🏴‍☠️                ║
{Colors.ENDC}"""
        print(banner)

    def get_user_id(self, username, session_id):
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
        try:
            response = self.session.get(url, headers=self.headers, cookies={'sessionid': session_id}, timeout=30)
            if response.status_code != 200: return None
            data = response.json()
            return data["data"]["user"]["id"]
        except: return None

    def get_user_info(self, user_id, session_id):
        url = f'https://i.instagram.com/api/v1/users/{user_id}/info/'
        try:
            response = self.session.get(url, headers=self.headers, cookies={'sessionid': session_id}, timeout=30)
            return response.json().get("user", {})
        except: return {}

    def get_followers(self, user_id, session_id, count=10):
        url = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count={count}'
        try:
            response = self.session.get(url, headers=self.headers, cookies={'sessionid': session_id}, timeout=30)
            return response.json().get("users", [])[:count]
        except: return []

    def get_recent_posts_and_comments(self, user_id, session_id, post_count=10):
        url = f'https://i.instagram.com/api/v1/feed/user/{user_id}/'
        posts_data = []
        all_commenters = []
        
        try:
            response = self.session.get(url, headers=self.headers, cookies={'sessionid': session_id}, timeout=30)
            items = response.json().get("items", [])[:post_count]
            
            for item in items:
                code = item.get("code")
                post_url = f"https://www.instagram.com/p/{code}/" if code else "N/A"
                
                post_info = {
                    "id": item.get("id"),
                    "url": post_url,
                    "caption": item.get("caption", {}).get("text", "Sem legenda") if item.get("caption") else "Sem legenda",
                    "location": item.get("location", {}).get("name", "Nenhuma") if item.get("location") else "Nenhuma",
                    "lat": item.get("location", {}).get("lat") if item.get("location") else None,
                    "lng": item.get("location", {}).get("lng") if item.get("location") else None,
                    "timestamp": datetime.fromtimestamp(item.get("taken_at")).strftime('%d/%m/%Y %H:%M'),
                    "likes": item.get("like_count"),
                    "comments_count": item.get("comment_count")
                }
                posts_data.append(post_info)
                
                if item.get("comment_count", 0) > 0:
                    comment_url = f'https://i.instagram.com/api/v1/media/{item.get("id")}/comments/'
                    comm_resp = self.session.get(comment_url, headers=self.headers, cookies={'sessionid': session_id}, timeout=30)
                    comments = comm_resp.json().get("comments", [])
                    for c in comments:
                        all_commenters.append(c.get("user", {}).get("username"))
            
            top_commenters = Counter(all_commenters).most_common(10)
            return posts_data, top_commenters
        except: return [], []

    def generate_pdf(self, data, filename):
        pdf = PDFReport()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # 1. Perfil
        pdf.chapter_title('1. RESUMO DO PERFIL ALVO')
        pdf.set_font('Arial', '', 11)
        profile = data['profile']
        fields = [
            ('Username', f"@{profile.get('username')}"),
            ('Nome Completo', profile.get('full_name')),
            ('ID do Usuario', profile.get('pk')),
            ('Seguidores', f"{profile.get('follower_count', 0):,}"),
            ('Seguindo', f"{profile.get('following_count', 0):,}"),
            ('Privado', 'Sim' if profile.get('is_private') else 'Nao'),
            ('Verificado', 'Sim' if profile.get('is_verified') else 'Nao'),
            ('Biografia', profile.get('biography', 'N/A'))
        ]
        for label, value in fields:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(40, 8, f"{label}:", 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 8, clean_text(str(value)), 0, 'L')

        # 2. Top 10 Seguidores
        pdf.ln(5)
        pdf.chapter_title('2. TOP 10 SEGUIDORES RECENTES')
        pdf.set_font('Arial', '', 10)
        if not data['followers']:
            pdf.cell(0, 8, "Nenhum seguidor encontrado ou perfil privado.", 0, 1)
        for follower in data['followers']:
            line = f" @{follower.get('username')} - {follower.get('full_name')}"
            pdf.cell(0, 7, clean_text(line), 0, 1)

        # 3. Top 10 Comentadores
        pdf.ln(5)
        pdf.chapter_title('3. ANÁLISE DE ENGAJAMENTO (TOP COMENTADORES)')
        pdf.set_font('Arial', '', 10)
        if not data['top_commenters']:
            pdf.cell(0, 8, "Nenhum comentario analisado.", 0, 1)
        for user, count in data['top_commenters']:
            line = f" @{user}: {count} comentarios nas ultimas postagens"
            pdf.cell(0, 7, clean_text(line), 0, 1)

        # 4. Localizacao e Metadados
        pdf.add_page()
        pdf.chapter_title('4. GEOLOC E ULTIMAS ATIVIDADES')
        pdf.set_font('Arial', '', 9)
        if not data['posts']:
            pdf.cell(0, 8, "Nenhuma postagem encontrada.", 0, 1)
        for post in data['posts']:
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(0, 6, f"Data: {post['timestamp']} | Likes: {post['likes']} | Comentarios: {post['comments_count']}", 0, 1)
            
            # Link da Postagem
            pdf.set_font('Arial', 'U', 9)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 6, f"Link: {post['url']}", 0, 1, link=post['url'])
            pdf.set_text_color(0, 0, 0)
            
            pdf.set_font('Arial', 'I', 9)
            loc = post['location']
            if post['lat']: loc += f" (Lat: {post['lat']}, Lng: {post['lng']})"
            pdf.cell(0, 6, clean_text(f"Localizacao: {loc}"), 0, 1)
            
            pdf.set_font('Arial', '', 9)
            caption = post['caption'][:150] + "..." if len(post['caption']) > 150 else post['caption']
            pdf.multi_cell(0, 5, clean_text(f"Legenda: {caption}"), border='B')
            pdf.ln(3)

        pdf.output(filename)
        return filename

    def run_interactive(self):
        self.print_banner()
        username = input(f"{Colors.OKGREEN} Username do Instagram (sem @): {Colors.ENDC}").strip().lstrip('@')
        session_id = input(f"{Colors.OKGREEN} Session ID: {Colors.ENDC}").strip()
        
        if not username or not session_id:
            print(f"{Colors.FAIL}Erro: Username e Session ID sao obrigatórios.{Colors.ENDC}")
            return

        print(f"\n{Colors.OKCYAN} Coletando dados de @{username}... Isso pode levar alguns segundos.{Colors.ENDC}")
        
        user_id = self.get_user_id(username, session_id)
        if not user_id:
            print(f"{Colors.FAIL}Erro: Nao foi possivel encontrar o usuario ou Session ID invalido.{Colors.ENDC}")
            return

        profile = self.get_user_info(user_id, session_id)
        followers = self.get_followers(user_id, session_id)
        posts, top_commenters = self.get_recent_posts_and_comments(user_id, session_id)

        data = {
            "profile": profile,
            "followers": followers,
            "posts": posts,
            "top_commenters": top_commenters
        }

        filename = f"relatorio_{username}.pdf"
        try:
            self.generate_pdf(data, filename)
            print(f"\n{Colors.OKGREEN} Investigacao concluida com sucesso!{Colors.ENDC}")
            print(f"{Colors.BOLD} Relatorio gerado: {os.path.abspath(filename)}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Erro ao gerar PDF: {e}{Colors.ENDC}")

if __name__ == "__main__":
    investigator = InstagramInvestigatorV2()
    if len(sys.argv) > 2:
        username = sys.argv[1].lstrip('@')
        session_id = sys.argv[2]
        user_id = investigator.get_user_id(username, session_id)
        if user_id:
            posts, top_commenters = investigator.get_recent_posts_and_comments(user_id, session_id)
            data = {
                "profile": investigator.get_user_info(user_id, session_id),
                "followers": investigator.get_followers(user_id, session_id),
                "posts": posts,
                "top_commenters": top_commenters
            }
            investigator.generate_pdf(data, f"relatorio_{username}.pdf")
    else:
        investigator.run_interactive()
