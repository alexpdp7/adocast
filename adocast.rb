require "asciidoctor"
require "json"
require "pry"

# to add a breakpoint: binding.pry
#
# to clear attributes which mess us printing objects, use @attr = nil
#
# drop https://github.com/antonmedv/fx/releases/latest in ~/.local/bin or similar, then use:
#
# $ bundle exec ruby adocast.rb xxx.adoc | fx

module Asciidoctor
    class Document
        def as_json(*)
            {
                :type => :document,
                :attributes => self.attributes,
                :source_location => self.source_location,
                :blocks => self.blocks
            }
        end  

        def to_json(*)
            as_json.to_json
        end  
    end  

    class Section
        def as_json(*)
            {
                :type => :section,
                :attributes => self.attributes,
                :title => self.title,
                :id => self.id,
                :level => self.level,
                :source_location => self.source_location,
                :blocks => self.blocks
            }
        end  
        def to_json(*)
            as_json.to_json
        end  
    end  

    class Block
        def as_json(*)
            {
                :type => :block,
                :attributes => self.attributes,
                :content => self.content,
                :source_location => self.source_location,
                :blocks => self.blocks
            }
        end  
        def to_json(*)
            as_json.to_json
        end  
    end  

    class List
        def as_json(*)
            {
                :type => :list,
                :attributes => self.attributes,
                :source_location => self.source_location,
                :blocks => self.blocks
            }
        end  
        def to_json(*)
            as_json.to_json
        end  
    end  

    class ListItem
        def as_json(*)
            {
                :type => :list_item,
                :attributes => self.attributes,
                :content => self.text,
                :source_location => self.source_location,
                :blocks => self.blocks
            }
        end  
        def to_json(*)
            as_json.to_json
        end  
    end  
end

doc = Asciidoctor.load_file ARGV[0], { :sourcemap => true, :backend => "docbook" }
puts doc.to_json
