-- ============================================================
-- portfolio.db CRUD 실습 쿼리
-- 사용법: VS Code에서 쿼리 블록을 선택 후 실행
-- ============================================================


-- ============================================================
-- 0. 테이블 생성 (처음 한 번만 실행)
-- ============================================================

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    email      TEXT    NOT NULL,
    message    TEXT    NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 1. CREATE — 데이터 삽입
-- ============================================================

-- 기본 삽입
INSERT INTO messages (name, email, message)
VALUES ('홍길동', 'hong@example.com', '포트폴리오 정말 멋집니다!');

-- 여러 행 한 번에 삽입
INSERT INTO messages (name, email, message) VALUES
    ('김철수', 'kim@example.com',  '협업 제안드리고 싶습니다.'),
    ('이영희', 'lee@example.com',  '프로젝트 문의드립니다.'),
    ('박민준', 'park@example.com', '연락 기다리겠습니다.');


-- ============================================================
-- 2. READ — 데이터 조회
-- ============================================================

-- 전체 조회
SELECT * FROM messages;

-- 최신순 정렬
SELECT * FROM messages
ORDER BY created_at DESC;

-- 특정 ID 조회
SELECT * FROM messages
WHERE id = 1;

-- 이름으로 검색 (부분 일치)
SELECT * FROM messages
WHERE name LIKE '%홍%';

-- 이메일로 검색
SELECT * FROM messages
WHERE email = 'hong@example.com';

-- 원하는 컬럼만 조회
SELECT id, name, email FROM messages;

-- 건수 확인
SELECT COUNT(*) AS 총건수 FROM messages;

-- 최근 3건만 조회
SELECT * FROM messages
ORDER BY created_at DESC
LIMIT 3;


-- ============================================================
-- 3. UPDATE — 데이터 수정
-- ============================================================

-- 특정 ID의 이름 수정
UPDATE messages
SET name = '홍길동(수정)'
WHERE id = 1;

-- 특정 ID의 여러 컬럼 동시 수정
UPDATE messages
SET name    = '김철수(수정)',
    message = '수정된 메시지입니다.'
WHERE id = 2;

-- 수정 결과 확인
SELECT * FROM messages WHERE id IN (1, 2);


-- ============================================================
-- 4. DELETE — 데이터 삭제
-- ============================================================

-- 특정 ID 삭제
DELETE FROM messages
WHERE id = 1;

-- 특정 이메일 삭제
DELETE FROM messages
WHERE email = 'park@example.com';

-- 전체 삭제 (주의! 되돌릴 수 없음)
-- DELETE FROM messages;

-- 삭제 후 확인
SELECT * FROM messages;


-- ============================================================
-- 5. 테이블 정보 확인
-- ============================================================

-- 테이블 구조 확인
PRAGMA table_info(messages);

-- DB 안의 모든 테이블 목록
SELECT name FROM sqlite_master WHERE type = 'table';

-- AUTO INCREMENT 현재 값 확인
SELECT * FROM sqlite_sequence;
