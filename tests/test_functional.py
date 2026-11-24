import pytest
from src.manager import Manager
from src.models import Parameters, Transfer

def test_tenants_settlements_sum_matches_apartment_costs():
    manager = Manager(Parameters())
    apartment_key = 'apart-polanka'
    year = 2026
    month = 11

    apartment_costs = manager.get_apartment_costs(apartment_key, year, month)
    assert apartment_costs is not None

    apartment_settlement = manager.get_settlement(apartment_key, year, month)
    assert apartment_settlement is not None
    assert apartment_settlement.total_due_pln == pytest.approx(apartment_costs)

    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)
    assert tenants_settlements is not None
    assert len(tenants_settlements) > 0

    total_tenants_due = sum(tenant_s.total_due_pln for tenant_s in tenants_settlements)
    assert total_tenants_due == pytest.approx(apartment_costs)

def test_get_debtors():
    manager = Manager(Parameters())
    assert manager.get_debtors('apart-polanka', 1, 2025) == []

    manager.transfers.extend([
        Transfer(amount_pln=100.0, date='2025-02-30', settlement_year=2025, settlement_month=2, tenant='tenant-1'),
        Transfer(amount_pln=200.0, date='2025-02-10', settlement_year=2025, settlement_month=2, tenant='tenant-1'),
        Transfer(amount_pln=2000.0, date='2025-02-05', settlement_year=2025, settlement_month=2, tenant='tenant-2')
    ])

    debtors = manager.get_debtors('apart-polanka', 2, 2025)
    assert debtors is not None
    assert {tenant.name for tenant in debtors} == {'Jan Nowak', 'Ewa Adamska'}

    assert manager.get_debtors('zpewnosciaprawdziwanazwamieszkania', 1, 2025) is None
    with pytest.raises(ValueError):
        manager.get_debtors('apart-polanka', 13, 2025)