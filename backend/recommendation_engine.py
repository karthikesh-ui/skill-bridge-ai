def readiness(skills, required, statuses, projects=0, interview=False):
    # Demo model only: 40% skills, 40% stages, 10% projects, 10% interview.
    skill_ratio = len(set(skills) & set(required)) / max(len(required), 1)
    progress = sum(1 for s in statuses if s == 'Completed') / max(len(statuses), 1)
    return round(40 * skill_ratio + 40 * progress + 10 * bool(projects) + 10 * bool(interview))
