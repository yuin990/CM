import pygame


class AtomPuzzle:
    def __init__(self):
        # 산소(Oxygen) 원자의 정답 위치 좌표를 정의합니다.
        self.solution_positions = [
            (200, 200), (400, 200), (600, 200),
            (200, 400), (600, 400),
            (200, 600), (400, 600), (600, 600)
        ]

    def check_puzzle_solution(self, electrons):
        # 현재 전자의 위치가 정답 위치와 모두 일치하는지 확인합니다.
        solution_count = 0
        for electron in electrons:
            if self.is_in_solution_zone(electron):
                solution_count += 1

        # 모든 전자가 정답 위치에 있다면 True를 반환합니다.
        return solution_count == len(self.solution_positions)

    def is_in_solution_zone(self, electron):
        # 특정 전자가 정답 위치에 있는지 확인하는 로직
        for solution_pos in self.solution_positions:
            # 전자의 위치와 정답 위치가 겹치는지 확인합니다.
            if electron.rect.collidepoint(solution_pos):
                return True
        return False