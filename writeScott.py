import argparse
import sys


def write_scotti(strain_data, pat_file, outfile):
    with open(outfile, 'w') as scotti:
        mdict = {}
        strain2patient = {} # dict of strain keys and patient entries
        strain2time = {}
        patient2time = {}
        with open(strain_data) as f:
            for line in f:
                mdict[line.split()[0]] = line.split()[1]
                strain2patient[line.split()[0]] = line.split()[2]
                strain2time[line.split()[0]] = line.split()[3]
        with open(pat_file) as f:
            for line in f:
                patient2time[line.split()[0]] = line.split()[1:]
        scotti.write('''<beast version='2.0' namespace='beast.evolution.alignment:beast.core:beast.core.parameter:beast.evolution.tree:beast.evolution.tree.coalescent:beast.core.util:beast.evolution.operators:beast.evolution.sitemodel:beast.evolution.substitutionmodel:beast.evolution.likelihood:beast.evolution.tree:beast.math.distributions:multitypetreeVolz.distributions:multitypetreeVolz.operators:multitypetreeVolz.util'>

   <alignment spec="beast.evolution.alignment.Alignment" id="alignment"
              dataType="nucleotide">
''')
        for i in mdict:
            scotti.write("<sequence taxon='" + i + "' value='" + mdict[i] + "' />\n")
        scotti.write('\n  </alignment>\n\n')
        scotti.write('''  <typeTraitSet spec='TraitSetWithLimits' id='typeTraitSet'
          traitname="type"
          value="''')
        first = True
        for i in strain2patient:
            if first:
                first = False
                scotti.write(i + '=' + strain2patient[i])
            else:
                scotti.write(', ' + i + '=' + strain2patient[i])
        scotti.write('''">
     <taxa spec='TaxonSet' alignment='@alignment'/>
   </typeTraitSet>\n\n''')
        scotti.write('''    <timeTraitSet spec='TraitSetWithLimits' id='timeTraitSet'
            traitname="date-forward"
            value="''')
        first = True
        for i in strain2time:
            if first:
                first = False
                scotti.write(i + '=' + strain2time[i])
            else:
                scotti.write(', ' + i + '=' + strain2time[i])
        scotti.write('''">
     <taxa spec='TaxonSet' alignment='@alignment'/>
   </timeTraitSet>\n\n''')
        scotti.write('''   <endInfectionsTraitSet spec='InfectionTraitSet' id='endInfectionsTraitSet' type='end'
          traitname="date-forward"
          value="''')
        first = True
        for i in patient2time:
            if first:
                first = False
                scotti.write(i + '=' + patient2time[i][1])
            else:
                scotti.write(', ' + i + '=' + patient2time[i][1])
        scotti.write('''">
          <taxaDates idref='timeTraitSet'/>
          <taxaTypes idref='typeTraitSet'/>
   </endInfectionsTraitSet>\n\n''')
        scotti.write('''   <startInfectionsTraitSet spec='InfectionTraitSet' id='startInfectionsTraitSet' type='start'
          traitname="date-forward"
          value="''')
        first = True
        for i in patient2time:
            if first:
                first = False
                scotti.write(i + '=' + patient2time[i][0])
            else:
                scotti.write(', ' + i + '=' + patient2time[i][0])
        scotti.write('''">
          <taxaDates idref='timeTraitSet'/>
          <taxaTypes idref='typeTraitSet'/>
   </startInfectionsTraitSet>''')
        scotti.write('''   <!-- Substitution model (HKY) -->
   <siteModel spec="SiteModel" id="siteModel">
     <mutationRate spec='RealParameter' id="mutationRate" value="1.0"/>
     <substModel spec="HKY">
       <kappa spec='RealParameter' id="hky.kappa" value="1.0"/>
       <frequencies estimate="false" spec='Frequencies'>
	 <frequencies spec='RealParameter' id="hky.freq" value="0.25 0.25 0.25 0.25"/>
       </frequencies>
     </substModel>
   </siteModel>

   <!-- Migration model -->
   <migrationModelUniform spec='MigrationModelUniform' id='migModel' minDemes=\'''' + str(len(patient2time)) + '''\'>
     <rate spec='RealParameter' value="0.001" dimension="1" id="rate"/>
     <popSize spec='RealParameter' value="1.0" dimension="1" id="popSize"/>
     <numDemes spec='IntegerParameter' value="40" dimension="1" id="numDemes" lower=\'''' + str(len(patient2time)) + '''\' upper=\'''' + str(len(patient2time) + 3) + '''\'/>
     <trait idref='startInfectionsTraitSet' type='start'/>
     <trait idref='endInfectionsTraitSet' type='end'/>
     <!--minDemes spec='Integer' value="4" dimension="1" id="minDemes"/-->
   </migrationModelUniform>

   <!-- Parameter priors -->
   <input spec='CompoundDistribution' id='parameterPriors'>
     <distribution spec='beast.math.distributions.Prior' x="@mutationRate">
       <distr spec='LogNormalDistributionModel' M="0.0" S="4.0"/>
     </distribution>

     <distribution spec='beast.math.distributions.Prior' x="@hky.kappa">
       <distr spec='LogNormalDistributionModel' M="0.0" S="4.0"/>
     </distribution>

     <!--distribution spec='beast.math.distributions.Prior' x="@rate">
       <distr spec='LogNormalDistributionModel' M="0.0" S="4.0"/>
     </distribution-->
     <distribution spec='beast.math.distributions.Prior' x="@rate">
       <distr spec='Exponential' mean="0.001"/>
     </distribution>
     <distribution spec='beast.math.distributions.Prior' x="@popSize">
       <distr spec="LogNormalDistributionModel"  M="0.0" S="4.0"/>
     </distribution>


     <!--distribution spec='beast.math.distributions.Prior' x="@numDemes">
       <distr spec='Poisson' lambda="30.0"/>
     </distribution-->
   </input>

   <!-- Probability of sequence data given tree -->
   <input spec='TreeLikelihood' id="treeLikelihood">
     <data idref="alignment"/>
     <tree idref="tree"/>
     <siteModel idref='siteModel'/>
   </input>

   <!-- Probability of tree given migration rates and population sizes -->
   <input spec='StructuredCoalescentTreeDensityConcise' id='treePrior'>
     <multiTypeTreeConcise idref="tree"/>
     <migrationModelUniform idref="migModel"/>
   </input>


   <run spec="MCMC" id="mcmc" chainLength="100000000" storeEvery="1000">

     <init spec='StructuredCoalescentMultiTypeTreeConcise' id='tree' nTypes="40">
         <migrationModelUniform spec='MigrationModelUniform' minDemes='10'>
             <rate spec='RealParameter' value="0.001" dimension="1"/>
             <popSize spec='RealParameter' value="1.0" dimension="1"/>
             <numDemes spec='IntegerParameter' value="40" dimension="1"/>
     		 <!--minDemes spec='Integer' value="4" dimension="1"/-->
         </migrationModelUniform>
         <trait idref='typeTraitSet'/>
         <trait idref='timeTraitSet'/>
     </init>

     <state>
       <stateNode idref="tree"/>
       <stateNode idref="rate"/>
       <stateNode idref="popSize"/>
       <stateNode idref="numDemes"/>
       <stateNode idref="mutationRate"/>
       <stateNode idref="hky.kappa"/>
       <stateNode idref="hky.freq"/>
     </state>

     <distribution spec='CompoundDistribution' id='posterior'>
       <distribution idref="treeLikelihood"/>
       <distribution idref='treePrior'/>
       <distribution idref="parameterPriors"/>
     </distribution>


     <!-- parameter scaling operators -->

  <!--  -->
     <operator spec='ScaleOperator' id='RateScaler'
 	      parameter="@rate"
 	      scaleFactor="0.8" weight="1">
     </operator>


    <!--    -->
     <operator spec="ScaleOperator" id="PopSizeScaler"
 	      parameter="@popSize"
	      scaleFactor="0.8" weight="1"/>

	 <!--    -->
     <operator spec="ShortRangeUniformOperator" id="NumDemesScaler"
 	      parameter="@numDemes" weight="1"/>

   <!--   -->
     <operator spec="ScaleOperator" id="muRateScaler"
	       parameter="@mutationRate"
	       scaleFactor="0.8" weight="1"/>


     <operator spec='ScaleOperator' id='kappaScaler'
	       parameter="@hky.kappa"
	       scaleFactor="0.8" weight="0.1">
     </operator>


 <!-- -->
     <operator spec="DeltaExchangeOperator" id="freqExchanger"
	       parameter="@hky.freq"
	       delta="0.01" weight="0.1"/>


<!--
     <operator spec="UpDownOperator" id="upDown"
               scaleFactor="0.8" weight="1">
       <up idref="popSize"/>
       <down idref="mutationRate"/>
       <down idref="rate"/>
     </operator>-->





	<!-- Multi-type tree operators	-->
     <operator id='treeScaler.t' spec='ScaleOperator' scaleFactor="0.5" weight="3" tree="@tree"/>
     <operator id='treeRootScaler.t' spec='ScaleOperator' scaleFactor="0.5" weight="3" tree="@tree" rootOnly='true'/>
     <operator id='UniformOperator.t' spec='Uniform' weight="30" tree="@tree"/>
     <operator id='SubtreeSlide.t' spec='SubtreeSlide' weight="15" gaussian="true" size="1.0" tree="@tree"/>
     <operator id='narrow.t' spec='Exchange' isNarrow='true' weight="15" tree="@tree"/>
     <operator id='wide.t' spec='Exchange' isNarrow='false' weight="3" tree="@tree"/>
     <operator id='WilsonBalding.t' spec='WilsonBalding' weight="3" tree="@tree"/>


     <!-- Multi-type tree operators

     <operator spec='TypedSubtreeExchangeUniform' id='STX'
 	      weight="10" multiTypeTree="@tree"/>


     <operator spec="TypedWilsonBaldingUniform" id="TWB"
 	      weight="10" multiTypeTree="@tree" alpha="0.2"/>


     <operator spec="MultiTypeUniformVolz" id="MTU"
	       weight="10" multiTypeTree="@tree"
	       includeRoot="true"
	       rootScaleFactor="0.9"/>


     <operator spec="MultiTypeTreeScaleVolz" id="MTTS1"
 	      weight="10" multiTypeTree="@tree"
 	      scaleFactor="0.98" useOldTreeScaler="true">
         <parameter idref="popSize"/>
         <parameterInverse idref="rate"/>
         <parameterInverse idref="mutationRate"/>
     </operator>


     <operator spec="MultiTypeTreeScaleVolz" id="MTTS2"
 	      weight="10" multiTypeTree="@tree"
 	      scaleFactor="0.98" useOldTreeScaler="true">
     </operator>
  -->



     <!-- Loggers -->

     <logger logEvery="10000" fileName="SCOTTI_FMDV.log">
       <model idref='posterior'/>
       <log idref="posterior"/>
       <log idref="treeLikelihood"/>
       <!--log idref="treePrior"/-->
       <log idref="migModel"/>
       <log idref="mutationRate"/>
       <log idref="hky.kappa"/>
       <log idref="hky.freq"/>
       <log spec='TreeHeightLogger' tree='@tree'/>
       <!--log spec='TreeLengthLogger' tree='@tree'/-->
       <!--log spec='TreeRootTypeLoggerVolz' multiTypeTreeVolz="@tree"/-->
     </logger>

     <logger logEvery="10000" fileName="SCOTTI_FMDV.trees" mode="tree">
       <log idref='treePrior'/>
     </logger>

     <!--logger logEvery="10000" fileName="/Users/nicolademaio/Desktop/structuredCoalescentConcise_example.trees">
       <log spec='TreeLoggerConcise' StructuredCoalescentTreeDensityConcise='@treePrior'/>
     </logger-->

     <!--logger logEvery="10000" fileName="/Users/nicolademaio/Desktop/structuredCoalescentConcise_example2.trees" mode="tree">
       <log idref="tree"/>
     </logger-->

     <logger logEvery="10000">
       <model idref='posterior'/>
       <log idref="posterior"/>
       <log idref="treeLikelihood"/>
       <!--log idref="treePrior"/-->
       <log spec='TreeHeightLogger' tree='@tree'/>
       <log idref="migModel"/>
       <log idref="mutationRate"/>
       <log idref="hky.kappa"/>
       <!--log idref="hky.freq"/-->
       <ESS spec='ESS' name='log' arg="@treePrior"/>
       <ESS spec='ESS' name='log' arg="@posterior"/>
       <!--ESS spec='ESS' name='log' arg="@rateMatrix"/-->
     </logger>

     <!--logger logEvery="1" fileName="/Users/nicolademaio/Desktop/structuredCoalescentConcise_example_transHistory.log">
       <log spec='MigrationHistoryLoggerUniform' density='@treePrior'/>
     </logger-->
   </run>

 </beast>''')


write_scotti(sys.argv[1], sys.argv[2], sys.argv[3])