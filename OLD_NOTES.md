October 6, 2014
============
I decided to use version of rosetta based off 6d932ff303d68daf86275e847d6f3c6edb5c6843 for this project.  This version is not in the master branch.  Normally I would want to use a version from the master branch, but in this case I have important changes in a personal branch that will take some significant effort to merge with master due to the recent pointer refactor.  Thus, in the interest of time, I merged the last commit to master before the pointer refactor into my personal branch.

My personal branch contained improvements to the refactored loop modeling code.  In particular, the version of the refactored loop modeling code in my branch is capable of fully reproducing next-gen KIC (NGK), while the version in master is not.  This is significant because it is very likely that we will want to combine NGK and KIC with fragments (KWF) in this project.

Note that commit 6d932f is the merge commit between master and my personal branch.  The actual version of rosetta we will use for this project will feature a few minor changes to support combining NGK and KWF, and so will probably be a few commits more advanced.  Once I have determined the final version, I will note that here.

Since our initial NGK validation runs have shown that NGK has issues recapitulating the terminal helix of the loop, we will have to use KWF also for the validation runs. 

October 7, 2014
============
Last night I found that RNA is not included in the default residue type set.  This was causing our preliminary loopmodel runs to crash.  I was able to fix the problem by copying the fullatom RNA residue type parameters (including pramas files and patch files) into the centroid type set directory.  Note that this seemed to be what was done for the centorid DNA parameters, which were already present.  I committed and merged the changes I made into master, because it seemed to me that rosetta should support RNA in centroid mode by default.  To see exactly what changes I made, look for commit 52e65474d8dcc99b90a17bd39841d547e829f558.

Today I also launched a set of preliminary jobs meant to gauge the feasibility of the project and to help pick a good loop region for future simulations.  We would like to identify loop endpoints that are likely to be relatively well fixed in real life.  We identified a number of such points using our intuition:

Starts:
1339: just after a long a-helix
1348: just before the b-turn
1354: just after the b-turn

Ends:
1363: just before a small a-helix
1369: just after a small a-helix

The preliminary simulation looked at 32 loops: 16 starting at every residue from 1339-1354 and ending at 1363, and 16 more ending at 1369.  Each loop was simulated using KIC with fragments and score function ramping.

October 9, 2014
============
The results from the preliminary simulations are coming in.  The loopmodel simulations were unable to recover the wildtype loop structure for any of the start/end points we chose.  For most of the longer loops, the loop slipped out from between the RNA/DNA and the rest of the protein and was just sticking out into space.  I think this failure mode probably had a lot to do the the initial loop building step.  There were probably a lot more ways to build an initial loop sticking out into space than to build one tucked into the major groove, and once the initial model was build the energy barrier between it and the right structure was too high.  I think in this case we might be able to skip initial loop building.  Of course we know the native loop structure, and we're not trying to move that far away from it.  So it makes sense to start in the native well.  The problem is that this may make us less likely to find competing minima far away from the native conformation.  But this is just a hard problem, and we can reduce the likelihood of creating such minima by only designing a handful of residues.

October 10, 2014
=============
I just launched a series of simulations with the initial build stage and the centroid stage both disabled.  For this set of simulations I also used a more limited set of loops: just the six combinations of start and end points listed above.

October 12, 2014
=============
The simulations with both the initial build stage and the centroid stage disabled finished.  For all six loops, almost exclusively sub-angstrom models were sampled.  On one hand, this is what we were hoping to see. On the other hand, it suggests that we may never be getting out of the native state basin at all.  To see if we could get greater breadth, we kicked of a set of simulation on the same 6 loops as before, this time with the initial build disabled but both the centroid and fullatom stages enabled.

October 13, 2014
=============
The centroid+fullatom simulations finished.  They all still find the native well (including the 31-residue loop) but they do show greater breadth than the fullatom-only simulations.  We decided to use centroid+fullatom from here on out.  We also made the decision to use the 31-residue loop.  Presently each loopmodel run on the 31-residue loop takes 8h on average.  (This may be an underestimate due to the 12h runtime limit.)

October 14, 2014
=============
We're taking a two-pronged approach to picking a PAM sequence to design for.  The first prong is a literature search and the second is simulation.  Roland was able to find a number of papers discussing the PAM specificity of Cas9.  From those papers, it seems like any sequence other than GG and (to a lesser extent) GA and AG will not be recognized by wildtype Cas9.  

This experimental evidence has more weight than simulations would, but we're running simulations anyways.  I guess because they were easy to run and we didn't have anything else to spend CPUs on at the moment.  We're running two kinds of simulations: one using just fixbb and one using loopmodel.  We launched 16 jobs for each kind of simulation, one for each possible combination of two base pairs (including the wildtype GG).  Our goal is to see which PAM sequence rosetta predicts that wildtype Cas9 will have the least affinity for.

I also took the loopmodel simulations as a chance to experiment with reducing the number of iterations loopmodel simulation.  The default (used previously) was to run 5 score function cycles and 310 temperature cycles.  I reduced this the 3 and 200, just 40% of the previous number.  I now expect each simulation to take about 3h, rather than 8h.  Still slow, but more manageable.

Today I also worked to find amino acid/DNA binding motifs.  We took a database of such motifs from the supplementary material of Havranek and Baker, Protein Science 2009, Vol 18:1293-1305.  These motifs were expressed in internal coordinates, so I had to convert them to cartesian coordinates as described in the supplement.  We only considered the "single" motifs, of which there were about 2000.  However, many of these did not look believable.  I expect that we will have to use our intuition to pick between motifs in the end.

October 15, 2014
=============
Today Roland and I put a lot of thought into picking which PAM sequence to design for, which protein motif to use, and which positions to allow to design.  Once we had made these decisions, I was able to launch the loop building jobs.

We decided to target the AA PAM sequence.  Again, the wildtype PAM sequence is GG.  Zhang et al., Scientific Reports, Vol 4:5405 investigated the specificity of Cas9 for all 16 PAM sequences.  They found that Cas9 only interacted appreciably with GG and GA, so we had a pretty free hand in choosing an orthogonal PAM sequence.  We chose AA for a few reasons.  First, Cas9 proteins in other species are known to bind AA, so we know going in that the design can be done.  Second, AA doesn't change the position of the purines relative to the pyrimidines.  This is good, because wildtype Cas9 interacts only with the purines.  This makes sense, because the purines are bigger and present a more specific constellation of H-bonding partners.  By keeping the purines in the same place, our designs can continue to interact the purines without having to adopt significantly different loop conformations.  Third, there may be minor groove interactions between a Lys and one of the C's from the wildtype GG.  T makes the same minor groove contacts as C, so by targeting the AA PAM we shouldn't have to worry about the minor groove.

We decided the use a QQ protein motif to bind with the AA PAM.  The database of DNA motifs we used contained motifs between adenine and 8 different amino acids: Asn, Asp, Gln, Glu, His, Ser, Thr, Tyr.  For every amino acid except Asn, Gln, and Tyr, there were no clear clusters of good-looking motifs and many of the motifs were obviously clashing with the nucleotide.  Tyr didn't have a big cluster of motifs, but it was believable.  Asn and Gln were by far the most common (although the input database was not screened for redundancy) and featured the same geometry.  The dominant motif for Asn and Gln made two H-bonds with the base, while the Tyr motif made just one.  Considering all this, we decided to use Gln for our design.  We chose Gln over Asn because it's longer, and the wildtype residue being replaced is Arg.  Choosing Gln minimizes how far the loop has to move relative to the wildtype Cas9.

We chose which positions to design by inspecting the structure and using our intuition.  All residue numbers referenced below are in rosetta numbering, meaning that the first residue of chain A is 1, the second is 2, and so on with no skips.  Unless otherwise noted, any residue except Cys and His was allowed at designable positions.  We excluded Cys because we didn't want to worry about weird oxidation chemistry and we excluded His because we didn't want any pH sensitive behavior.  We wanted to minimize the number of positions we allowed to design, because successful computational designs typically don't make more than ~10-15 mutations.  Furthermore, my experience from the KSI project is that making WT reversions after the fact in a tedious and not very fruitful process.  In the end, we picked 11 positions to design (counting the two Arg->Gln mutations).

1347,1354: These residues are parallel to each other in the b-turn and are facing toward the helical bundle.  We let the design so that they could potentially get bulkier and push the loop further away from the helices and closer to the DNA.  However, because we really want to preserve the b-turn geometry, we limited the design to residues with high b-sheet propensity:  TVIYFWM.

1356-1359: These residues surround the two Arg->Gln mutations.  We allowed them to design because this is the part of the loop backbone that needs to change conformation the most.  To decrease the chances of our designs interacting with the wildtype PAM (GG), we didn't allow these positions to mutate to Arg (or Cys or His).

1344-1345: These positions are right behind 1356-1359 stretch that interacts with the DNA.  We allowed them design so that they could become bulkier and push the Glns closer to the DNA.

1253: In wildtype Cas9, this position is an Asp that is clearly helping to position one of the Args interacting with the DNA.  Because this is a position with the capacity to help stabilize the one of the sidechains interacting with DNA, we allowed it to design so that it could specialize for Gln.

1309,1312: These two positions are in the helical bundle right behind the loop.  We allowed them to design so that they could become bulkier and push the loop out towards the DNA.  These position were not allowed to become Pro or Gly (or Cys or His) because we wanted to make sure we didn't break the helices.

Having made all these decisions, I was able to kick off 10,000 loopbuilding jobs.  The jobs were as described above: the initial build stage was skipped, the centroid stage was not, 3 sfxn cycles and 200 temp cycles were used.

October 17, 2014
=============
Today the model building jobs finished, but I realized that I forgot to turn on -ex1 -ex2 -extrachi_cutoff 0 flags.  This was an unacceptable mistake, so I had to restart the jobs.  However, this ended up being a nice way to test the strength of the restraints I was using.  I want the restraints to be strong enough to move the backbone and put the sidechain where I want them, but not so strong that I get unrealistic backbones.  The results from the "no -ex1 -ex2" jobs showed that most of the models were within 0.5A - 2.0A of the targeted positions.  This is about the mix of sub-angstrom/not sub-angstrom that I look for, so I was happy with the constraint weights.  It may be worth noting that I actually optimized the restraint weights when I did this for KSI, but for this project I just used the same weights that worked the best for KSI.

October 19, 2014
=============
Today the model building jobs finished.  Of the 9939 models that were built, I picked 6036 to design.  The criterion I used to pick models were: 

loop_rmsd < 2.0A: The designs with really big loop rmsds usually featured the beta-turn peeling away from the helices, which didn't seem realistic.

restraint_dist < 1.0A: This is just to select for models that actually put the Glns where they need to be.  I used a tighter 0.6A cutoff for the KSI project, but I decided to use a more relaxed cutoff here because I don't think wer need as much accuracy.

dunbrack_score < 4.0: Very few models were eliminated by this filter.  I just didn't want to go forward with designs requiring unrealistic sidechain confromations.

delta_buried_unsat_hbonds < 4: Surprisingly, the majority of structures had fewer buried unsatisfied H-bonds that the wildtype structure.  I suspect this may be related to the fact that the wildtype structure is at 2.5A resolution, which is good but not great.  This gave me less confidence in this metric, which is why I chose a more relaxed cutoff of 4 instead 0.  It's also worth noting that even structures with buried unsat counts above the cutoff looked reasonable and scored well.

I generated 20 designs for each model I picked.

October 20, 2014
=============
The design jobs finished over night.  For some reason the design simulation didn't seem to acknoledge the restraints, so maybe 30% of the designs moved one of both of the Glns out of position.  I'll fix this for the next round of design, but for now it wasn't a big problem because there were still lots of designs with the desired Gln geometry.  I picked 50 designs using the boltzmann weighting scheme, with a temperature of 3 and a restraint_dist cutoff of 0.75A.  Roland and I decided that to make the restraint_dist cutoff more strict because we had plenty of designs below 0.75A.

With designs in hand, I launched the validation simulations.  For each of the 50 designs that were picked, 500 simulations were launched.  As with the model building simulations, I reduced the number of iterations to 3 sfxn cycles and 200 temp cycles and skipped the initial build stage.  Unlike the model building simulations, I decided to use NGK instead of KWF.  The primary reason for this is that I have more confidence in validation result generated by a different algorithm than was used to generate the models in the first place.  It was also faster to get NGK running, because I didn't need to  generate 50 fragement libraries first.

October 22, 2014
=============
After we looked at some of the incoming results from the validation simulations, we realized that NGK was doing a poor job of simulating the 31-residue loop.  We didn't design any residues towards the ends of the loops, so we would expect those to mostly stay in place.  In particular, the small alpha-helical turn on the C-terminal end of the loop is very insulaated from any design positions.  However, NGK consistently turned this structure into a poorly packed loop.  Thus even the models that scored well and put the Glns close to the desired position were unbelievable, because parts of those models that should be fairly statis had always moved a lot. We already know that KWF doesn't suffer from this problem because of the results from the wildtype and model building simulations.  So we decided that we had to restart the validation runs using KWF.

During the model building simulations, I had noticed that each job was using twice as much memory as a typical loop modeling job (2Gb rather than 1Gb).  I thought the difference might have be due to the fragment library.  Even though we were only using enough fragments to cover about 50 residues, we were still generating and storing enough fragments to cover the entire 1000 residue protein, which could take up 1Gb of memory.  Roland proposed a method of generating truncated fragment files that we could use to both generate fragments faster and to significantly reduce the memory overhead.  With a lot of help from Shane, we quickly implemented this method and used it to build fragments for our KWF validation simulations.  It took about 4h to build the truncated fragment libraries, while the full library took about 24h to build.  The memory usage for the validation jobs also returned to the expected (1Gb) level.  We believe that this improvement to the fragment library generation protocol will be useful in any project that uses fragments for loop modeling.

October 23, 2014
=============
We weren't able to restart the validation jobs until today because it took us a while to debug our new fragment generation pipeline.  But we started the jobs today with all the same parameters as the original validation jobs, except the sampling algorithm is KWF instead of NGK.

October 26, 2014
=============
The first round of validation jobs finished today.  For 6/50 of the designs, the lowest scoring decoy had a sub-angstrom restraint distance.  However, none of these designs had a convincing funnel.   The wildtype control simulation had a much tighter funnel than any of the designs.  All combined, the validation simulations generated 146 decoys with subangstrom restraint distances.  These were chosen to carry on with another round of design and validation.  I generated 100 designs per backbone, for a total of 14600 designs.  Again, it seemed like the restraints weren't turned on in the design simulation because the Gln sidechains flipped out of place in 10%-15% of the designs.  I thought I'd fixed this problem after the first round of design, but I guess I hadn't.  The design finished in about an hour, but I was unable to get the fragment library generation scripts to run.

October 27, 2014
================
Today, with help from Shane,  I was able to get the fragment generation scripts running.  That code is still being developed with the features mentioned a few days ago, and it's not really stable yet.

October 28, 2014
================
Today I started the second round of validation jobs.

November 1, 2014
================
The second round of validation jobs finished today.  I would classify 17 of the designs as having promising funnels, although I didn't do any analysis to determine how similar those designs were.  That said, even these promising designs all had score vs rmsd funnels that were much more diffuse than the wildtype funnel.  That isn't necessarily a problem; in principle only the lowest scoring decoy matters.  But I would have more confidence in these designs if the funnels looked more native.

I think that the best way to do that is to allow more positions to design.  Aloowing more positions to design is always a trade-off.  One one hand, it makes you more likely to find a sequence that stabilizes the local conformation you're looking for.  On the other hand, it makes it more likely that there will be some sort of confounding global change that your simulations couldn't account for.  Since our funnels weren't looking very native, I felt that we were most likely on the "too few design positions" part of the spectrum.

I decided to allow residues 1349-1352 to design to anything except histidine and cysteine.  The exceptions were made for the standard reasons mentioned a few weeks ago.  These 4 residues make up the turn in the beta-hairpin.  I decided to let them mutate for a few reasons.  First, many of our designs change the conformation of this turn by moving Phe1350 into the slot previously occupied by Tyr1349, and using Tyr1349 to push the loop closer towards the DNA.  If the conformation is going to change, I think we should allow the sequence to change along with it.  Second, we were previously hesitant to mutate these residue because we thought that they were part of a b-turn motif.  In fact, they are not.  I looked into this closely when I was trying to decide which mutations to allow, and I found the b-turns have conserved glycines or prolines, which this turn does not.  According to a motif search on PDBeMotif, this turn is actually a niche-3r, which I've never heard of.  I decided to let it mutate to almost anything so that it could turn into a true b-turn, if it wants to.

For this third round of design with the turn allowed to mutate, I used as input the subangstrom structures from the second round of validation.  There were 839 of these structures.  For each I generated 100 designs.  The design simulations were started today.

November 2, 2014
================
The design simulations finished early this morning.  There were 21668 unique designs out of 83899 total.  I used to Boltzmann weighting scheme with a temperature of 5 to pick 50 designs to validate.  I chose the temperature to give a CDF that wasn't too sharp (I don't want to validate the same design over and over) or too flat.  This round required a higher temperature that previous rounds, although I don't know if that's significant.  I then launched the fragment generation jobs for the 50 launched jobs.

