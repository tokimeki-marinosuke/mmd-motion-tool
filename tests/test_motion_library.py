"""src/motions/library.py のテスト。"""

from pathlib import Path

from motions.library import MotionEntry, MotionLibrary, create_sample_catalog


def test_add_and_all():
    library = MotionLibrary()
    entry = MotionEntry(path=Path("sample_motions/wave_happy.vmd"), action="wave", emotion="happy")
    library.add(entry)

    assert library.all() == [entry]


def test_entry_referenced_file_need_not_exist():
    # メタデータ管理のみを扱うため、参照先のVMDファイルが実在しなくても登録できる
    entry = MotionEntry(path=Path("does/not/exist.vmd"), action="wave", emotion="happy")
    library = MotionLibrary([entry])

    assert library.all() == [entry]


def test_default_intensity_is_one():
    entry = MotionEntry(path=Path("x.vmd"), action="wave", emotion="happy")
    assert entry.intensity == 1.0


def test_create_sample_catalog_contains_expected_examples():
    library = create_sample_catalog()
    entries = library.all()

    assert len(entries) == 3
    tags = {(e.action, e.emotion) for e in entries}
    assert tags == {("wave", "happy"), ("bow", "polite"), ("turn_back", "shy")}


def test_find_by_action():
    library = create_sample_catalog()
    results = library.find_by_action("wave")

    assert len(results) == 1
    assert results[0].emotion == "happy"


def test_find_by_emotion():
    library = create_sample_catalog()
    results = library.find_by_emotion("shy")

    assert len(results) == 1
    assert results[0].action == "turn_back"


def test_search_with_both_filters():
    library = create_sample_catalog()
    results = library.search(action="bow", emotion="polite")

    assert len(results) == 1
    assert results[0].path == Path("sample_motions/bow_polite.vmd")


def test_search_with_no_filters_returns_all():
    library = create_sample_catalog()
    assert library.search() == library.all()


def test_search_with_no_match_returns_empty():
    library = create_sample_catalog()
    assert library.search(action="unknown") == []
