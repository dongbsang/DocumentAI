import React from 'react';
import '../css/ReceiptView.css';

/**
 * 영수증 전용 렌더링 컴포넌트
 */
const ReceiptView = ({ data }) => {
  if (!data) {
    return <div className="error-message">영수증 데이터가 없습니다.</div>;
  }

  const { summary, details, meta } = data;
  const { payment, merchant, items } = details || {};

  // 금액 포맷팅 함수
  const formatCurrency = (amount) => {
    if (amount === null || amount === undefined) return '-';
    return new Intl.NumberFormat('ko-KR').format(amount) + '원';
  };

  // 날짜 포맷팅 함수
  const formatDate = (datetime) => {
    if (!datetime) return '-';
    return datetime.replace('T', ' ').substring(0, 19);
  };

  // 사업자번호 포맷팅 (XXX-XX-XXXXX)
  const formatBusinessId = (id) => {
    if (!id || id.length !== 10) return id;
    return `${id.substring(0, 3)}-${id.substring(3, 5)}-${id.substring(5)}`;
  };

  return (
    <div className="receipt-view">
      {/* 요약 카드 */}
      <div className="summary-card">
        <div className="summary-header">
          <h2 className="summary-title">{summary?.title || '영수증'}</h2>
          <span className={`status-badge ${summary?.status?.type || 'info'}`}>
            {summary?.status?.label || '정상'}
          </span>
        </div>
        <div className="summary-amount">{summary?.subtitle || '-'}</div>
        <div className="summary-datetime">
          📅 {formatDate(summary?.datetime || payment?.datetime)}
        </div>
        {summary?.description && (
          <div className="summary-description">{summary.description}</div>
        )}
      </div>

      {/* 결제 정보 섹션 */}
      {payment && (
        <section className="info-section">
          <h3 className="section-title">💳 결제 정보</h3>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">결제 금액</span>
              <span className="info-value highlight">
                {formatCurrency(payment.amount_total)}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">결제 방법</span>
              <span className="info-value">{payment.payment_method || '-'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">카드사</span>
              <span className="info-value">{payment.card_company || '-'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">카드 브랜드</span>
              <span className="info-value">{payment.card_brand || '-'}</span>
            </div>
            {payment.installment && (
              <div className="info-item">
                <span className="info-label">할부</span>
                <span className="info-value">{payment.installment}</span>
              </div>
            )}
            <div className="info-item">
              <span className="info-label">승인번호</span>
              <span className="info-value">{payment.approval_number || '-'}</span>
            </div>
            <div className="info-item">
              <span className="info-label">승인상태</span>
              <span className="info-value">{payment.approval_status || '-'}</span>
            </div>
            {payment.transaction_type && (
              <div className="info-item">
                <span className="info-label">거래유형</span>
                <span className="info-value">{payment.transaction_type}</span>
              </div>
            )}
            {payment.currency && (
              <div className="info-item">
                <span className="info-label">통화</span>
                <span className="info-value">{payment.currency}</span>
              </div>
            )}
            {payment.amount_supply !== null && (
              <div className="info-item">
                <span className="info-label">공급가액</span>
                <span className="info-value">{formatCurrency(payment.amount_supply)}</span>
              </div>
            )}
            {payment.amount_vat !== null && (
              <div className="info-item">
                <span className="info-label">부가세</span>
                <span className="info-value">{formatCurrency(payment.amount_vat)}</span>
              </div>
            )}
            {payment.service_fee > 0 && (
              <div className="info-item">
                <span className="info-label">봉사료</span>
                <span className="info-value">{formatCurrency(payment.service_fee)}</span>
              </div>
            )}
          </div>
        </section>
      )}

      {/* 가맹점 정보 섹션 */}
      {merchant && (
        <section className="info-section">
          <h3 className="section-title">🏪 가맹점 정보</h3>
          <div className="info-grid">
            <div className="info-item full-width">
              <span className="info-label">상호명</span>
              <span className="info-value">{merchant.name || '-'}</span>
            </div>
            {merchant.category && (
              <div className="info-item">
                <span className="info-label">업종</span>
                <span className="info-value">{merchant.category}</span>
              </div>
            )}
            {merchant.representative && (
              <div className="info-item">
                <span className="info-label">대표자</span>
                <span className="info-value">{merchant.representative}</span>
              </div>
            )}
            {merchant.business_id && (
              <div className="info-item full-width">
                <span className="info-label">사업자번호</span>
                <span className="info-value">{formatBusinessId(merchant.business_id)}</span>
              </div>
            )}
            {merchant.address && (
              <div className="info-item full-width">
                <span className="info-label">주소</span>
                <span className="info-value">{merchant.address}</span>
              </div>
            )}
            {merchant.tel && (
              <div className="info-item">
                <span className="info-label">전화번호</span>
                <span className="info-value">{merchant.tel}</span>
              </div>
            )}
          </div>
        </section>
      )}

      {/* 구매 내역 섹션 */}
      {items && items.length > 0 && (
        <section className="info-section">
          <h3 className="section-title">🛒 구매 내역</h3>
          <div className="items-list">
            {items.map((item, index) => (
              <div key={index} className="item-card">
                <div className="item-header">
                  <span className="item-number">{index + 1}</span>
                  <span className="item-name">{item.name || '상품명 없음'}</span>
                </div>
                <div className="item-details">
                  <div className="item-detail">
                    <span className="detail-label">수량</span>
                    <span className="detail-value">{item.quantity || 0}개</span>
                  </div>
                  <div className="item-detail">
                    <span className="detail-label">단가</span>
                    <span className="detail-value">{formatCurrency(item.unit_price)}</span>
                  </div>
                  <div className="item-detail">
                    <span className="detail-label">합계</span>
                    <span className="detail-value highlight">
                      {formatCurrency(item.total_price)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 메타 정보 섹션 */}
      {meta && (
        <section className="info-section meta-section">
          <h3 className="section-title">ℹ️ 추가 정보</h3>
          <div className="info-grid">
            {meta.pg_provider && (
              <div className="info-item">
                <span className="info-label">PG사</span>
                <span className="info-value">{meta.pg_provider}</span>
              </div>
            )}
            {meta.source && (
              <div className="info-item">
                <span className="info-label">출처</span>
                <span className="info-value">{meta.source}</span>
              </div>
            )}
            {meta.transaction_id && (
              <div className="info-item full-width">
                <span className="info-label">거래ID</span>
                <span className="info-value">{meta.transaction_id}</span>
              </div>
            )}
          </div>
        </section>
      )}
    </div>
  );
};

export default ReceiptView;
