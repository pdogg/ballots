# ballots
Python PoC of a cryptographically verifiable paper voting system

IMPORTANT DISCLAIMER: This was a weekend project. It may contain serious flaws which make it fit for no purpose other than experimentation and novelty. Please do not use it at scale or in the real world without proper due-diligence. I am also aware of the presence of public and private keys in this repository. You shouldn’t use those keys. There are also a host of other security issues present here such as leaking of all of the ballot private keys to the file system during the ballot rendering process. That is bad.

This is a proof of concept experimental implementation of a paper ballot voting system which attempts to solve for some problems associated with current methods of verifying the legitimacy of ballot voting systems. The main goal of the project is to create a paper ballot which is auditable, verifiable (by the voter), tamper evident, and protected from the possibility of counterfeit ballot printing. Most importantly, the system preserves the secrecy and anonymity of the individual vote.

In this system each jurisdiction would generate a public / private key pair, individual ballots are then generated with public / private key pairs. The election jurisdiction’s private key is used to sign the public key of the individual ballots. Thus, at counting time the ballot can be verified as genuinely a product of the election jurisdiction, or an entity authorized by that jurisdiction (in possession of the jurisdiction’s private key). Key pairs and signatures are stored on the ballot and receipt page as QR codes. A voter is given the receipt page for their ballot which contains the private key.

<img width="615" alt="picture" src="https://user-images.githubusercontent.com/2677122/202910296-a876ee74-a6e7-49bd-bcd5-c761f69f8ad5.png">

A vote is counted as normal but with an additional step of encrypting the vote contents with the public key on the ballot. The private key, known only to the voter with the receipt could later be produced and used to verify that the vote was received and recorded according to the voter’s wishes. Several voters could group together to verify large numbers of ballots and votes were received and correctly counted. Each individual vote is still anonymous unless the voter reveals the corresponding private key.

<img width="837" alt="picture2" src="https://user-images.githubusercontent.com/2677122/202910301-850b2e1d-b661-4e57-9dea-df3413a7d92e.png">

ballottest.py should be fairly self-evident as the basic set of functions required to generate, validate, and “count” votes in this system. Counting of the actual votes themselves is left out of the POC as I was focused on conceptually validating the use of printed QR codes and key pairs for the purposes of demonstrating solutions to the “other” problems around paper ballot election integrity.

Please feel free to use this code and concept for any purpose you wish have fun and maybe make the world a better place.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

