DID_SOV_QqEfJxe752NCmWqR5TssZ5 = {
    "@context": "https://www.w3.org/ns/did/v1",
    "id": "did:bid:QqEfJxe752NCmWqR5TssZ5",
    "verificationMethod": [
        {
            "id": "did:bid:QqEfJxe752NCmWqR5TssZ5#key-1",
            "type": "Ed25519VerificationKey2018",
            "controller": "did:bid:QqEfJxe752NCmWqR5TssZ5",
            "publicKeyBase58": "DzNC1pbarUzgGXmxRsccNJDBjWgCaiy6uSXgPPJZGWCL",
        }
    ],
    "authentication": ["did:bid:QqEfJxe752NCmWqR5TssZ5#key-1"],
    "assertionMethod": ["did:bid:QqEfJxe752NCmWqR5TssZ5#key-1"],
    "service": [
        {
            "id": "did:bid:QqEfJxe752NCmWqR5TssZ5#did-communication",
            "type": "did-communication",
            "serviceEndpoint": "http://localhost:3002",
            "recipientKeys": ["did:bid:QqEfJxe752NCmWqR5TssZ5#key-1"],
            "routingKeys": [],
            "priority": 0,
        }
    ],
}
