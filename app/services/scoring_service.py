class ScoringService:
    @staticmethod
    def calculate_score(data):
        score = 0
        role = data.get('role', '').lower()
        company = data.get('company', '').lower()

        # Priorização baseada no seu README
        if any(keyword in role for keyword in ['recruiter', 'tech lead', 'manager']):
            score += 50
        elif 'developer' in role or 'engineer' in role:
            score += 30
        
        # Bônus para stacks Python (Foco do projeto)
        if 'python' in role or 'backend' in role:
            score += 20

        return min(score, 100)