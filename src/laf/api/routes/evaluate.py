from fastapi import APIRouter

from laf.governance.models import EvaluateRequest, EvaluateResponse
from laf.governance.policy_engine import evaluate as eval_policy
from laf.storage.audit_log import log_evaluation

router = APIRouter()

@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest) -> EvaluateResponse:
    allowed, risk, violations, redactions, sanitized, audit = eval_policy(req)

    # persist audit (best-effort; should never break API)
    try:
        log_evaluation(
            input_text=req.input_text,
            data_classification=req.data_classification,
            allowed=allowed,
            risk_score=risk,
            violations=[v.model_dump() for v in violations],
            redactions_applied=redactions,
            sanitized_text=sanitized,
            audit_trail=audit,
        )
    except Exception:
        pass

    return EvaluateResponse(
        allowed=allowed,
        risk_score=risk,
        violations=violations,
        redactions_applied=redactions,
        sanitized_text=sanitized,
        audit_trail=audit,
    )
