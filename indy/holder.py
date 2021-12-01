"""Base Indy Holder class."""

from abc import ABC, ABCMeta, abstractmethod
from typing import Tuple, Union

from ..core.error import BaseError
from ..ledger.base import BaseLedger


class IndyHolderError(BaseError):
    """Base class for holder exceptions."""


class IndyHolder(ABC, metaclass=ABCMeta):
    """Base class for holder."""

    RECORD_TYPE_MIME_TYPES = "attribute-mime-types"
    CHUNK = 256

    def __repr__(self) -> str:
        """
        Return a human readable representation of this class.

        Returns:
            A human readable string for this class

        """
        return "<{}>".format(self.__class__.__name__)

    @abstractmethod
    async def get_credential(self, credential_id: str) -> str:
        """
        Get a credential stored in the wallet.

        Args:
            credential_id: Credential id to retrieve

        """

    @abstractmethod
    async def credential_revoked(
            self, ledger: BaseLedger, credential_id: str, fro: int = None, to: int = None
    ) -> bool:
        """
        Check ledger for revocation status of credential by cred id.

        Args:
            credential_id: Credential id to check

        """

    @abstractmethod
    async def delete_credential(self, credential_id: str):
        """
        Remove a credential stored in the wallet.

        Args:
            credential_id: Credential id to remove

        """

    @abstractmethod
    async def get_mime_type(
            self, credential_id: str, attr: str = None
    ) -> Union[dict, str]:
        """
        Get MIME type per attribute (or for all attributes).

        Args:
            credential_id: credential id
            attr: attribute of interest or omit for all

        Returns: Attribute MIME type or dict mapping attribute names to MIME types
            attr_meta_json = all_meta.tags.get(attr)

        """

    @abstractmethod
    async def create_presentation(
            self,
            presentation_request: dict,
            requested_credentials: dict,
            schemas: dict,
            credential_definitions: dict,
            rev_states: dict = None,
    ) -> str:
        """
        Get credentials stored in the wallet.

        Args:
            presentation_request: Valid indy format presentation request
            requested_credentials: Indy format requested credentials
            schemas: Indy formatted schemas JSON
            credential_definitions: Indy formatted credential definitions JSON
            rev_states: Indy format revocation states JSON
        """

    @abstractmethod
    async def create_credential_request(
            self, credential_offer: dict, credential_definition: dict, holder_did: str
    ) -> Tuple[str, str]:
        """
        Create a credential request for the given credential offer.

        Args:
            credential_offer: The credential offer to create request for
            credential_definition: The credential definition to create an offer for
            holder_did: the DID of the agent making the request

        Returns:
            A tuple of the credential request and credential request metadata

        """

    @abstractmethod
    async def store_credential(
            self,
            credential_definition: dict,
            credential_data: dict,
            credential_request_metadata: dict,
            credential_attr_mime_types=None,
            credential_id: str = None,
            rev_reg_def: dict = None,
    ):
        """
        Store a credential in the wallet.

        Args:
            credential_definition: Credential definition for this credential
            credential_data: Credential data generated by the issuer
            credential_request_metadata: credential request metadata generated
                by the issuer
            credential_attr_mime_types: dict mapping attribute names to (optional)
                MIME types to store as non-secret record, if specified
            credential_id: optionally override the stored credential id
            rev_reg_def: revocation registry definition in json

        Returns:
            the ID of the stored credential

        """

    @abstractmethod
    async def create_revocation_state(
            self,
            cred_rev_id: str,
            rev_reg_def: dict,
            rev_reg_delta: dict,
            timestamp: int,
            tails_file_path: str,
    ) -> str:
        """
        Create current revocation state for a received credential.

        Args:
            cred_rev_id: credential revocation id in revocation registry
            rev_reg_def: revocation registry definition
            rev_reg_delta: revocation delta
            timestamp: delta timestamp

        Returns:
            the revocation state

        """
