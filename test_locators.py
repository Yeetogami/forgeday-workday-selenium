"""Locator contract — no browser required."""

from locators import Locators


class TestLocatorContract:
    def test_every_locator_targets_data_automation_id(self) -> None:
        skipped = {"WORK_ADD"}
        for name, value in vars(Locators).items():
            if name.startswith("_") or name.endswith("_VARIANTS") or name in skipped:
                continue
            if isinstance(value, str):
                assert "data-automation-id" in value, name

    def test_country_selector_is_not_a_substring_trap(self) -> None:
        assert Locators.COUNTRY.endswith("='country']")
        assert "countryRegion" not in Locators.COUNTRY
        assert "countryPhoneCode" not in Locators.COUNTRY

    def test_sign_in_with_email_is_catalogued(self) -> None:
        assert "signInWithEmail" in Locators.SIGN_IN_WITH_EMAIL
