"""
Filters set the base query that gets passed to the storage adapter.
"""


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, chatterbot, session_id):
        """
        Because this is the base filter class, this method just
        returns the storage adapter's base query. Other filters
        are expected to override this method.
        """
        return chatterbot.storage.base_query


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive responses to prevent
    a chat bot from repeating statements that it has recently said.
    """

    def filter_selection(self, chatterbot, session_id):

        text_of_recent_responses = []

        # TODO: Add a larger quantity of response history
        text_of_recent_responses.append(
            chatterbot.storage.get_latest_response(session_id)
        )

        # Return the query with no changes if there are no statements to exclude
        if not text_of_recent_responses:
            return super(RepetitiveResponseFilter, self).filter_selection(
                chatterbot,
                session_id
            )

        query = chatterbot.storage.base_query.statement_text_not_in(
            text_of_recent_responses
        )

        return query
