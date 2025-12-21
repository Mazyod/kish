"""Tests for the Team enum."""

import kish


def test_team_values():
    """Test Team enum values."""
    assert int(kish.Team.White) == 0
    assert int(kish.Team.Black) == 1


def test_team_opponent():
    """Test Team.opponent() returns the other team."""
    assert kish.Team.White.opponent() == kish.Team.Black
    assert kish.Team.Black.opponent() == kish.Team.White


def test_team_opponent_involution():
    """Test that opponent of opponent is self."""
    assert kish.Team.White.opponent().opponent() == kish.Team.White
    assert kish.Team.Black.opponent().opponent() == kish.Team.Black


def test_team_str():
    """Test Team string representation."""
    assert str(kish.Team.White) == "White"
    assert str(kish.Team.Black) == "Black"


def test_team_repr():
    """Test Team repr."""
    assert repr(kish.Team.White) == "Team.White"
    assert repr(kish.Team.Black) == "Team.Black"


def test_team_equality():
    """Test Team equality."""
    assert kish.Team.White == kish.Team.White
    assert kish.Team.Black == kish.Team.Black
    assert kish.Team.White != kish.Team.Black


def test_team_hash():
    """Test Team is hashable."""
    teams = {kish.Team.White, kish.Team.Black}
    assert len(teams) == 2
    assert kish.Team.White in teams
    assert kish.Team.Black in teams
