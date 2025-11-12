import React from 'react';
import '../css/GenericView.css';

/**
 * 기타 문서 전용 렌더링 컴포넌트 (진단서, etc)
 */
const GenericView = ({ data, category }) => {
  if (!data) {
    return <div className="error-message">문서 데이터가 없습니다.</div>;
  }

  const { summary, details, meta } = data;

  // 객체를 보기 좋게 렌더링하는 함수
  const renderObject = (obj, level = 0) => {
    if (!obj || typeof obj !== 'object') {
      return <span className="value-text">{String(obj)}</span>;
    }

    if (Array.isArray(obj)) {
      return (
        <div className="array-container" style={{ marginLeft: `${level * 20}px` }}>
          {obj.map((item, index) => (
            <div key={index} className="array-item">
              <span className="array-index">{index + 1}.</span>
              {renderObject(item, level + 1)}
            </div>
          ))}
        </div>
      );
    }

    return (
      <div className="object-container" style={{ marginLeft: `${level * 20}px` }}>
        {Object.entries(obj).map(([key, value]) => (
          <div key={key} className="object-item">
            <span className="object-key">{key}:</span>
            <div className="object-value">{renderObject(value, level + 1)}</div>
          </div>
        ))}
      </div>
    );
  };

  // 카테고리별 아이콘 및 제목
  const getCategoryInfo = () => {
    switch (category) {
      case 'diagnosis':
        return { icon: '🏥', title: '진단서' };
      case 'etc':
      default:
        return { icon: '📄', title: '문서' };
    }
  };

  const categoryInfo = getCategoryInfo();

  return (
    <div className="generic-view">
      {/* 요약 카드 */}
      <div className="summary-card">
        <div className="summary-header">
          <h2 className="summary-title">
            {categoryInfo.icon} {summary?.title || categoryInfo.title}
          </h2>
          {summary?.status && (
            <span className={`status-badge ${summary.status.type || 'info'}`}>
              {summary.status.label}
            </span>
          )}
        </div>
        {summary?.subtitle && (
          <div className="summary-subtitle">{summary.subtitle}</div>
        )}
        {summary?.datetime && (
          <div className="summary-datetime">📅 {summary.datetime}</div>
        )}
        {summary?.description && (
          <div className="summary-description">{summary.description}</div>
        )}
      </div>

      {/* 상세 정보 섹션 */}
      {details && (
        <section className="info-section">
          <h3 className="section-title">📋 상세 정보</h3>
          <div className="details-content">
            {renderObject(details)}
          </div>
        </section>
      )}

      {/* 메타 정보 섹션 */}
      {meta && Object.keys(meta).length > 0 && (
        <section className="info-section">
          <h3 className="section-title">ℹ️ 추가 정보</h3>
          <div className="meta-content">
            {renderObject(meta)}
          </div>
        </section>
      )}
    </div>
  );
};

export default GenericView;
