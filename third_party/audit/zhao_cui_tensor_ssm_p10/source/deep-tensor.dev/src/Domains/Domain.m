classdef Domain
    
    properties
        bound
    end
    
    methods
        function [x,dxdz] = reference2domain(obj, z)
            error('Domain:abstractMethod', 'reference2domain must be implemented by a subclass');
        end
        function [z,dzdx] = domain2reference(obj, x)
            error('Domain:abstractMethod', 'domain2reference must be implemented by a subclass');
        end
        function [logdxdz,logdxdz2] = reference2domain_log_density(obj, z)
            error('Domain:abstractMethod', 'reference2domain_log_density must be implemented by a subclass');
        end
        function [logdzdx,logdzdx2] = domain2reference_log_density(obj, x)
            error('Domain:abstractMethod', 'domain2reference_log_density must be implemented by a subclass');
        end
    end
    
    
    methods
        function y = domain(obj)
            y = obj.bound;
        end
        
        function y = domain_left(obj)
            y = obj.bound(1);
        end

        function y = domain_right(obj)
            y = obj.bound(2);
        end
    end
end
