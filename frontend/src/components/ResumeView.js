import React from 'react';
import '../css/ResumeView.css';

/**
 * 이력서 전용 렌더링 컴포넌트
 */
const ResumeView = ({ data }) => {
  if (!data) {
    return <div className="error-message">이력서 데이터가 없습니다.</div>;
  }

  const { summary, details } = data;
  const { personal, education, experience, skills, certifications, languages, projects } = details || {};

  // 날짜 포맷팅
  const formatDate = (date) => {
    if (!date) return '-';
    return date;
  };

  // 기간 포맷팅
  const formatPeriod = (start, end) => {
    if (!start) return '-';
    return `${formatDate(start)} ~ ${end === 'present' || end === '현재' ? '현재' : formatDate(end)}`;
  };

  return (
    <div className="resume-view">
      {/* 요약 카드 */}
      <div className="summary-card">
        <h2 className="summary-title">{summary?.title || '이력서'}</h2>
        {summary?.subtitle && (
          <div className="summary-subtitle">{summary.subtitle}</div>
        )}
        {summary?.description && (
          <div className="summary-description">{summary.description}</div>
        )}
        {summary?.status && (
          <span className={`status-badge ${summary.status.type || 'info'}`}>
            {summary.status.label}
          </span>
        )}
      </div>

      {/* 인적사항 섹션 */}
      {personal && (
        <section className="info-section">
          <h3 className="section-title">👤 인적사항</h3>
          <div className="info-grid">
            {personal.name && (
              <div className="info-item">
                <span className="info-label">이름</span>
                <span className="info-value highlight">{personal.name}</span>
              </div>
            )}
            {personal.birth_date && (
              <div className="info-item">
                <span className="info-label">생년월일</span>
                <span className="info-value">{formatDate(personal.birth_date)}</span>
              </div>
            )}
            {personal.gender && (
              <div className="info-item">
                <span className="info-label">성별</span>
                <span className="info-value">{personal.gender}</span>
              </div>
            )}
            {personal.email && (
              <div className="info-item full-width">
                <span className="info-label">이메일</span>
                <span className="info-value">{personal.email}</span>
              </div>
            )}
            {personal.phone && (
              <div className="info-item">
                <span className="info-label">연락처</span>
                <span className="info-value">{personal.phone}</span>
              </div>
            )}
            {personal.address && (
              <div className="info-item full-width">
                <span className="info-label">주소</span>
                <span className="info-value">{personal.address}</span>
              </div>
            )}
          </div>
        </section>
      )}

      {/* 학력 섹션 */}
      {education && education.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">🎓 학력</h3>
          <div className="timeline-list">
            {education.map((edu, index) => (
              <div key={index} className="timeline-item">
                <div className="timeline-marker">{index + 1}</div>
                <div className="timeline-content">
                  <div className="timeline-header">
                    <h4 className="timeline-title">{edu.school || '학교명 없음'}</h4>
                    <span className="timeline-period">
                      {formatPeriod(edu.start_date, edu.end_date)}
                    </span>
                  </div>
                  {edu.major && (
                    <div className="timeline-detail">
                      <span className="detail-label">전공</span>
                      <span className="detail-value">{edu.major}</span>
                    </div>
                  )}
                  {edu.degree && (
                    <div className="timeline-detail">
                      <span className="detail-label">학위</span>
                      <span className="detail-value">{edu.degree}</span>
                    </div>
                  )}
                  {edu.status && (
                    <div className="timeline-detail">
                      <span className="detail-label">상태</span>
                      <span className="detail-value">{edu.status}</span>
                    </div>
                  )}
                  {edu.gpa && (
                    <div className="timeline-detail">
                      <span className="detail-label">학점</span>
                      <span className="detail-value">{edu.gpa}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 경력 섹션 */}
      {experience && experience.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">💼 경력</h3>
          <div className="timeline-list">
            {experience.map((exp, index) => (
              <div key={index} className="timeline-item">
                <div className="timeline-marker">{index + 1}</div>
                <div className="timeline-content">
                  <div className="timeline-header">
                    <h4 className="timeline-title">{exp.company || '회사명 없음'}</h4>
                    <span className="timeline-period">
                      {formatPeriod(exp.start_date, exp.end_date)}
                    </span>
                  </div>
                  {exp.position && (
                    <div className="timeline-detail">
                      <span className="detail-label">직책</span>
                      <span className="detail-value">{exp.position}</span>
                    </div>
                  )}
                  {exp.department && (
                    <div className="timeline-detail">
                      <span className="detail-label">부서</span>
                      <span className="detail-value">{exp.department}</span>
                    </div>
                  )}
                  {exp.description && (
                    <div className="timeline-description">{exp.description}</div>
                  )}
                  {exp.responsibilities && exp.responsibilities.length > 0 && (
                    <div className="timeline-list-detail">
                      <span className="detail-label">주요 업무</span>
                      <ul>
                        {exp.responsibilities.map((resp, i) => (
                          <li key={i}>{resp}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 기술 스택 섹션 */}
      {skills && skills.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">🛠️ 기술 스택</h3>
          <div className="skills-grid">
            {skills.map((skill, index) => (
              <div key={index} className="skill-item">
                <span className="skill-name">{skill.name || skill}</span>
                {skill.level && (
                  <span className="skill-level">{skill.level}</span>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 자격증 섹션 */}
      {certifications && certifications.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">📜 자격증</h3>
          <div className="list-items">
            {certifications.map((cert, index) => (
              <div key={index} className="list-item-card">
                <div className="list-item-header">
                  <span className="list-item-number">{index + 1}</span>
                  <span className="list-item-title">{cert.name || '자격증명 없음'}</span>
                </div>
                <div className="list-item-details">
                  {cert.issuer && (
                    <div className="list-item-detail">
                      <span className="detail-label">발급기관</span>
                      <span className="detail-value">{cert.issuer}</span>
                    </div>
                  )}
                  {cert.date && (
                    <div className="list-item-detail">
                      <span className="detail-label">취득일</span>
                      <span className="detail-value">{formatDate(cert.date)}</span>
                    </div>
                  )}
                  {cert.expiry_date && (
                    <div className="list-item-detail">
                      <span className="detail-label">만료일</span>
                      <span className="detail-value">{formatDate(cert.expiry_date)}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 어학 섹션 */}
      {languages && languages.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">🌏 어학</h3>
          <div className="info-grid">
            {languages.map((lang, index) => (
              <div key={index} className="info-item">
                <span className="info-label">{lang.language || '언어'}</span>
                <span className="info-value">{lang.level || '-'}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 프로젝트 섹션 */}
      {projects && projects.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">🚀 프로젝트</h3>
          <div className="timeline-list">
            {projects.map((project, index) => (
              <div key={index} className="timeline-item">
                <div className="timeline-marker">{index + 1}</div>
                <div className="timeline-content">
                  <div className="timeline-header">
                    <h4 className="timeline-title">{project.name || '프로젝트명 없음'}</h4>
                    {project.period && (
                      <span className="timeline-period">{project.period}</span>
                    )}
                  </div>
                  {project.role && (
                    <div className="timeline-detail">
                      <span className="detail-label">역할</span>
                      <span className="detail-value">{project.role}</span>
                    </div>
                  )}
                  {project.description && (
                    <div className="timeline-description">{project.description}</div>
                  )}
                  {project.technologies && project.technologies.length > 0 && (
                    <div className="timeline-tags">
                      {project.technologies.map((tech, i) => (
                        <span key={i} className="tag">{tech}</span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default ResumeView;
