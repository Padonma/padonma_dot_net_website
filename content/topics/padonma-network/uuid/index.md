---
title: UUID
summary: Using the UUID v4 standard to generate IDs ensures unique IDs assigned without any multiparty coordination or orgaization
---

[Understanding UUID: Purpose and Benefits of a Universal Unique Identifier](https://medium.com/@gaspm/understanding-uuid-purpose-and-benefits-of-a-universal-unique-identifier-59110154d897)

>Flip a coin 128 times and write down 1 for each head and 0 for each tail. This gives you a sequence of 128 1s and 0s, or 128 bits of randomness. That’s a space large enough that the probability of generating the same sequence twice is so extremely low that you can rule it out for practical purposes.
>
>How is that related to UUIDs? If you have ever seen a UUID then you know they look similar to this: 420cd09a-4d56-4749-acc2-40b2e8aa8c42. This format is just a textual representation of 128 bits. How does it work? The UUID string has 36 characters in total. If we remove the 4 dashes, which are there just to make it a bit more human-readable, we are left with 32 hexadecimal digits: 0-F. Each digit represents 4 bits and 32 * 4 bits = 128 bits. So UUIDs are 128-bit values. We often represent them as strings, but that's just a convenience.
>
>UUID has been explicitly designed to be unique and generated without coordination. When you have a good random generator then 128 random bits are enough to practically guarantee uniqueness. At the same time, 128 bits are not too much, so UUIDs do not occupy too much space when stored.
