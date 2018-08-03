package usersimproj;

import java.util.*;
import java.lang.*;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.ling.*;

import it.uniroma1.lcl.babelfy.commons.*;
import it.uniroma1.lcl.babelfy.core.*;
import it.uniroma1.lcl.babelfy.commons.annotation.SemanticAnnotation;
import it.uniroma1.lcl.babelnet.*;
import it.uniroma1.lcl.jlt.util.Language;

public class UserSimTest
{
    public static void main(String[] args)
    {
        try
        {
            // Step 1: Annotate input sentenses
            //CoreNLPWrap corenlp_1 = new CoreNLPWrap("Align, Disambiguate, and Walk is a WordNet-based approach for measuring semantic similarity of arbitrary pairs of lexical items, from word senses to full texts.", true);
            //CoreNLPWrap corenlp_1 = new CoreNLPWrap("In a move to reassert control over the party's seven senators, the national executive last night rejected Aden Ridgeway's bid to become interim leader, in favour of Senator Greig, a supporter of deposed leader Natasha Stott Despoja and an outspoken gay rights activist.", true);
            //CoreNLPWrap corenlp_1 = new CoreNLPWrap("Are you intentionally putting the cancellation date into the expirationDate field. Or should this be. GitHub repository for the SecureDrop whistleblower platform. Do not submit tips here.The PDB files are in their own sub directories so adding them manually to debugger would be extremely tedious , and I am not sure if even that is possible. Or you can build libcc on your own machine and then build electron with it , the paths to PDBs are hardcoded in object files so debugger should be able to find the correct PDB files. Maybe we should rename the application to crates registry. Could you merge this please.The CMake-built cphstats will not work properly until this is merged.", true);

            //CoreNLPWrap corenlp_2 = new CoreNLPWrap("Cash-strapped financial services group AMP has shelved a $400 million plan to buy shares back from investors and will raise $750 million in fresh capital after profits crashed in the six months to June 30.", false);
            
            /*
            corenlp_1.getDecomposedSentences();
            corenlp_1.getConstituentTrees();
            corenlp_2.getDecomposedSentences();
            corenlp_2.getConstituentTrees();
            List<DeSentence> l_sentences_1 = corenlp_1.getDeSentences();
            List<DeSentence> l_sentences_2 = corenlp_2.getDeSentences();
            */

            // Step 2: Fetch BabelNet synsets for tokens in sentenses
            /*
            BabelWrap bw = new BabelWrap(); 
            for(DeSentence sent : l_sentences_1)
            {
                boolean ret_getsynsets = true;
                ret_getsynsets = bw.getSynsets(sent);
                if(!ret_getsynsets)
                {
                    System.out.println("[ERR]: UserSimTest getSynsets() err!");
                }
            }*/
            /*for(DeSentence sent : l_sentences_2)
            {
                boolean ret_getsynsets = true;
                ret_getsynsets = bw.getSynsets(sent);
                if(!ret_getsynsets)
                {
                    System.out.println("[ERR]: UserSimTest getSynsets() err!");
                }
            }*/

            // Output
            /*
            ArrayList<DeToken> l_tokens_1 = null;
            //ArrayList<DeToken> l_tokens_2 = null;
            for(DeSentence sent_1 : l_sentences_1)
            {
                //System.out.println("[S1]");
                //System.out.println("    Orig: " + sent.getOrigSentence());
                l_tokens_1 = sent_1.getDeTokens();
                
                for(DeToken token_1 : l_tokens_1)
                {
                    System.out.println("    Token " + l_tokens_1.indexOf(token_1) + ": " 
                                            + "word = " + token_1.word() + ", "
                                         + "lemma = " + token_1.lemma() + ", "
                                         + "POS = " + token_1.pos() + ", "
                                         + "NER = " + token_1.ner()); 
                    System.out.print("    Synset = ");
                    if(token_1.synset() != null && token_1.synset().size() != 0)
                    {
                        String bn_synset = bw.m_babelnet.getSynset(new WordNetSynsetID("wn:"+token_1.synset().get(0))).getID().getSimpleOffset();
                        token_1.synset().forEach(sense->System.out.print(sense + ":" + bn_synset + " "));
                    }
                    else
                    {
                        System.out.print("No synset!");
                    }
                    System.out.println("");
                }
                System.out.println("-----------------------------------------");
                
            }
            */
            /*for(DeSentence sent_2 : l_sentences_2)
            {
                l_tokens_2 = sent_2.getDeTokens();
            }*/

            // ADW
            /*
            ADWWrap adw = new ADWWrap();
            for(DeToken token_1 : l_tokens_1)
            {
                List<String> l_offset_1 = token_1.synset();
                if(l_offset_1 == null || l_offset_1.size() == 0)
                {
                    System.out.println("[S1]" + token_1.word() + " has no synset!");
                    continue;
                }
                for(DeToken token_2 : l_tokens_2)
                {
                    List<String> l_offset_2 = token_2.synset();
                    if(l_offset_2 == null || l_offset_2.size() == 0)
                    {
                        System.out.println("[S2]" + token_2.word() + " has no synset!");
                    }
                    else
                    {
                        Double sim = adw.getWordPairSimilarity(l_offset_1, l_offset_2);
                        System.out.println("[S1]" + token_1.word() + ":" + "[S2]" + token_2.word() + ":" + sim.toString());
                    }
                }
            }
            */

            // Constituent Tree
            //System.out.println("----------------------------------------");
            //System.out.println("Consituent Trees:");
            //System.out.println("[S1]:");
            /*
            Tree testtree = Tree.valueOf("(S (NP I) (VP (V saw)) (NP him))");
            System.out.println(testtree.toString());
            List<Tree> leaves = testtree.getLeaves();
            LabelFactory slf = testtree.labelFactory();
            int i = 0;
            for(Tree leaf : leaves)
            {
                leaf.setLabel(slf.newLabel(leaf.value() + ":" + String.valueOf(i)));
                i += 1;
            }
            System.out.println(leaves.toString());
            StringBuilder strbldr = new StringBuilder();
            strbldr = corenlp_1.printTree(testtree, strbldr);
            System.out.println(strbldr.toString());
            */
            //System.out.println("");
            /*
            for(DeSentence sent1 : l_sentences_1)
            {
                System.out.println(sent1.getOrigSentence());
                Tree const_tree = sent1.getConstituentTree();
                System.out.println("[Orig Tree:]");
                //System.out.println(const_tree.toString());
                const_tree.pennPrint();
                System.out.println("[My Tree:]");
                System.out.println(sent1.printTaggedTree());
                System.out.println("[Tagged Tree:]");
                Tree tagged_tree = sent1.getTaggedTree();
                //System.out.println(tagged_tree.toString());
                tagged_tree.pennPrint();
                System.out.println("[Pruned Tree:]");
                Tree pruned_tree = sent1.getPrunedTree(true);
                pruned_tree.pennPrint();
                System.out.println(pruned_tree.toString());
                //strbldr = corenlp_1.printTree(const_tree, strbldr);
                //System.out.println(strbldr.toString());
                //const_tree.pennPrint();
                //System.out.println(const_tree.toString());
            }*/
            /*System.out.println("[S2]:");
            for(DeSentence sent2 : l_sentences_2)
            {
                System.out.println(sent2.getOrigSentence());
                Tree const_tree = sent2.getConstituentTree();
                System.out.println("[Orig Tree:]");
                System.out.println(const_tree.toString());
                System.out.println("[My Tree:]");
                System.out.println(corenlp_2.printTaggedTree(const_tree, sent2));
                //Tree const_tree = sent2.getConstituentTree();
                //const_tree.indexLeaves();
                //corenlp_2.printTree(const_tree);
                //const_tree.pennPrint();
                //System.out.println(sent2.getConstituentTree());
            }*/

            // clean up
            //corenlp_1.shutdownCoreNLPClient();
            //corenlp_2.shutdownCoreNLPClient();



            /**
             * User Text
             */
            UserTextIn uti = new UserTextIn("jdbc:sqlite:/home/fcmeng/gh_data/Events/201708/user_text_clean_2017_08_01_0.db");
            uti.processUserTextFromDB("pos5jkJAZofH00dC9RaEMw", "2017-08-01T00:00:00Z", "2017-08-02T00:00:00Z");
            uti.awaitShutdown();
        }
        catch(Exception e)
        {
            e.toString();
            e.printStackTrace();
        }

    }

}
