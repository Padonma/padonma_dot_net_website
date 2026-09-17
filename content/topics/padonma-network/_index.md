---
title: Padonma Network Intro
summary: "Handwoven QR tech for artisan textiles"
weight: 1
hero:
  image: "dotted-p-icon-r7-pinked-bigged.png"
---

once have uuid, can do all manner of fancy stuff, like write it on a piece of paper, put that tame alpanumeric character sequence on a web page that google crawls, blockchain, etc


The Padonma Network is exploring the possibility of tracking cottage
industry garments via handwoven QR codes. The goal is to design the
easiest on-ramp imaginable by which a single artisan could make their
products globally traceable via handmade QR codes.

The ancient handweaving technology of the rigid heddle loom seems like
it may well be fit for the purpose of handweaving rMQR ID bands. Read
the [Bandgrind Experiments](/bandgrinding.html) pages for a log of ongoing experiments into
weaving rMQR ID bands via a rigid heddle.

[![](sami_heddles.jpg)](https://durhamweaver64.blogspot.com/2015/01/travels-around-baltic-sami-weaving.html)

This project is exploring the potential of tagging garments with
handwoven labels containing rMQR codes, which are a novel variant of QR
codes. The rMQR specification was ratified as an ISO standard in May
of 2022. The name "rMQR code" is short for "rectangular Micro Quick Response
code." Whereas original style QR codes are square, rMQR codes are
narrow and rectangular, resembling ribbons or bands:

<img src="rmqr_example_r7_43.png" data-align="center" height="75" />

There are many prior examples of handcrafted QR codes being recongized
by QR reader software. The relative advantage of rMQR over QR in this
project is that while handweaving it is easier to weave seven "bits"
per row than the "wider" rows of traditional QR codes, and the
machinery required to do so is minimal ([fingerweaving](https://www.instructables.com/How-to-Fingerweave-Something/) would not even
require a loom). The goal is to make it as easy as possible for
artisans to join the Padonma Network.

It would seem like an rMQR code such as the one above could be
woven into textile bands which would look something like the small band in the
following example, but the black pattern "pixels" of the words would
be replaced with rMQR code data modules:

[![](jeannie_glaves_example_band.png)](https://spinoffmagazine.com/a-spinner-s-journey-in-inkle-bands/)

A simple rigid heddle backstrap loom would be sufficient to weave such
a band, which would look much like this exaple:

[![](r7_wide_band.png)](https://www.youtube.com/watch?v=dKLudDihe_I)

The weaving term "letter pick-up" refers to using pick-up techniques
to weave letters into bands. So this Padonma Network project is trying
to work out "QR code band pick-up weaving," or more succinctly "QR pick-up."


# Proposal


This proposal has a hardware part and a software part.

The hardware part is the bands with UUIDs encoded into rMQR codes
handwoven into them, which in the Padonma Network are called "rMQR ID
bands." Each garment has a unique UUID encoded in the rMQR code on its
ID band.

The software part is using a garment's unique UUID ID to represent the
garment in the digital domain. The same (UUID) ID can be used
consistently across both public and private databases. The same tag
would be used in both context.

For an example of private database, artisans could track their
inventory privately in a spreadsheet using the UUIDs. And when a
garment leaves from its place of manufacture the same UUID will
represent it outside in the wild. For an example of public database, a
blockchain could be used solely as a public domain global inventory
tracking system (not cryptocurrencies but garments will probably have
NFTs that contain garment UUIDs), using the same UUIDs to represent
garments globally.

Both parts of this proposal are addressed in the following subsections:



# Blockchain for Fashion
summary: India is already blockchain tracking handloomed sarees with embedded QRs

QR codes can encode any arbitrary digital data. In the use case of
Padonma, the QR code will encode the unique digitial ID of the garment
into which it is sewn. For Padonma, the digital ID data standard used
is called UUIDs, short for [Universally Unique Idenfifiers](https://en.wikipedia.org/wiki/Universally_unique_identifier). The garment
IDs can be tracked in a distribute inventory system, which for the
Padonma project would be implemented using blockchain technology.

In other words, the handspun QR code encodes the ID of the garment's
unique NFT. The NFT is simply the unique ID of the garment in the
distributed global inventory tracking system, which happens to be a
blockchain. (There are no overpriced JPEGs in this blockchain use
case.) This is how a handcrafted garment can be tracked in a global
inventory system as the garment travels the global supply chain.

A garment's physical tag will have its QR code handwoven into the
fabric, using simple techniques to make what weavers call bands (or
narrow wares, or ribbons). The encoded IDs correspond to NFT IDs, each
garment has its own NFT. The NFT is simply for inventory tracking
identity, think of it like a digital passport for the garment. This is not a
silly collectors game based on overpriced JPEGs. The NFT gives the
garment an identity in the distributed database that is the
blockchain, which serves as the inventory tracking system.

Each garment will have its own unique rMQR tag and own unique NFT. A
collection of such NFTs tracked on a blockchain are the distributed
equivalent for a factory inventory system that could span the entire
supply chain.




# Conclusion

The current goal is simply to prove that handwoven rMQR codes can be
easily scanned by mobile phone. Weaving experiments are currently
being done to figure out the cheapest, easiest, and quickest way to
handweave rMQR bands.

Once a garment is tagged with an rMQR band with a unique UUID encoded
in its QR code, all manner of interesting things can be done. The
rMQR band tags the garment with a unique UUID, and that UUID is the
garment's unique identity in the digital world.

"Rem QR ID band"

blockchains using rMQR tags.

As an example of one manner of interesting thing to do with **rMQR ID
bands**, the Padonma Network project hopes to explore globally
tracking garments via distributed web technnologies.

Perhaps web5 might be an elegant
solution – something involving blockchain for public info, and
artisans storing their private data in DWNs ([web5 DWNs data packbacks](https://www.youtube.com/watch?v=49BneqwfIOE&ab_channel=CertifiedFreshEvents)).

And the UUID in the rMQR ID band it what connects the garment's identity
in the public web, the blockchain, and the DWN private database.

Once inventory is on a blockchain, paying for garments with, say,
Bitcoin is certainly possible. Surely it should be possible to pay for
a garment by exchanging Bitcoin for a garment NFT. (Via web5?)

In India, the government already encourages paying for QR coded
handloom objects via digital money: [QR Codes in Handloom and Handicraft Industry: Make It More Vibrant](https://scanova.io/blog/qr-codes-in-handloom-handicraft/):

> Also, The Ministry of Textiles, Government of India, promotes
> digital transactions using BHIM app or Bharat QR Code. Bharat QR
> Code is one of the most popular QR Code-based mobile banking apps
> in India.

But the Padonma Network should use an open source blockchain to be run
publicly by artisans on their Android phones. And the only actually
valuable cryptocurrency is Bitcoin so, web5? (What does a
decentralized, blockchain-related, network-of-trust based global
inventory system working in a networkless jungle look like? A
blockchain network that keeps falling apart yet somehow comes to
consensus? Each (Android) node would run its own web5 inventory app?
Et cetera.)
