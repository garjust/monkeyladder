import logging
logger = logging.getLogger('monkeyladder')


def get_new_rank(ladder):
    """
    Returns the lowest current rank in the ladder
    """
    ranking = ladder.ranking()
    if ranking:
        return ranking[len(ranking) - 1].rank + 1
    return 1


def _validate_ranking_and_execute(ladder, function):
    for i, ranked_item in enumerate(ladder.ranking()):
        if ranked_item.rank != i + 1:
            function(ladder, ranked_item, i + 1)


def validate_ranking(ladder):
    """
    Validates the ladders ranked items have no inconsistencies (gaps, duplicates)
    """
    def raise_ranking_error_exception(ladder, ranked_item, correct_rank):
        raise AssertionError("Found invalid rank in ladder %s: %s" % (ladder, ranked_item))
    _validate_ranking_and_execute(ladder, raise_ranking_error_exception)


def correct_ranking(ladder):
    """
    Iterates through a ladders ranked items collapsing rank gaps and eliminating duplicates
    """
    def fix_ranked_item(ladder, ranked_item, correct_rank):
        logger.debug("Fixing rank of %s of ladder %s to %s" % (ranked_item, ladder, correct_rank))
        ranked_item.rank = correct_rank
        ranked_item.save()
    _validate_ranking_and_execute(ladder, fix_ranked_item)
